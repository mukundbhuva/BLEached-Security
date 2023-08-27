import struct
import os


def construct_message(service_id, name, msg):
    buffer = bytearray()
    buffer.extend(bytes([service_id, 0, 0]))
    buffer.extend(name.encode('utf-8'))
    buffer.append(ord(':'))
    buffer.extend(msg.encode('utf-8'))
    return buffer

def construct_call(service_id, name):
    buffer = bytearray()
    buffer.extend(bytes([service_id, 0, 0]))
    buffer.extend(name.encode('utf-8'))
    # buffer.append(ord(':'))
    # buffer.extend(msg.encode('utf-8'))
    return buffer

def get_protocol(b2, b3, b_arr):
    value_of = len(b_arr) + 8
    b_arr2 = bytearray()
    b_arr2.append(205 & 0xFF)
    b_arr2.extend(struct.pack('>I', value_of - 3)[2:])
    b_arr2.append(b2)
    b_arr2.append(1)
    b_arr2.append(b3)
    b_arr2.extend(struct.pack('>I', len(b_arr))[2:])
    b_arr2.extend(b_arr)
    return b_arr2


def int_to_bytes(i):
    return struct.pack('>I', i)


def extract_field(packet):
    return packet[2:].decode()


if __name__ == "__main__":
    services = {
        1: "SMS",
        2: "QQ",
        3: "WeChat",
        4: "Facebook",
        5: "Twitter",
        6: "Skype",
        7: "Line!",
        8: "WhatsApp",
        9: "Kakao Talk",
        16: "Instagram",
        17: "LinkedIn"
    }

    print("Select Messaging Service:")
    for service_id, service_name in services.items():
        print(f"{service_id} - {service_name}")

    service_id = int(input("Enter service ID: "))
    name = input("Enter Name: ")
    message = input("Enter Message: ")

    data = get_protocol(18, 18, construct_message(service_id, name, message))
    # data = get_protocol(18, 17, construct_call(1, name))

    first_packet = data[:20]
    second_packet = data[20:]

    # print("First Packet:")
    # print(first_packet.hex())

    # print("Second Packet:")
    # print(second_packet.hex())

    message_notifications_cmd_array = get_protocol(18, 7, bytes([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))

    print("Notification:")
    print(message_notifications_cmd_array.hex())
    
    # def switch_protocol(b2, b3, b4):
    #     return bytes([205, 0, 6, b2, 1, b3, 0, 1, b4])

    # def get_set_find_me_value():
    #     return switch_protocol(18, 11, 2)


    notif = "gatttool --device=CC:67:78:D4:1B:12 -t random --char-write-req  --handle=0x0023 --value=" + message_notifications_cmd_array.hex() + ";" 
    first = "gatttool --device=CC:67:78:D4:1B:12 -t random --char-write-req  --handle=0x0023 --value=" + first_packet.hex() + ";" 
    second = "gatttool --device=CC:67:78:D4:1B:12 -t random --char-write-req  --handle=0x0023 --value=" + second_packet.hex() + ";" 

    # print(get_set_find_me_value().hex())
    os.system(notif+first+second)
