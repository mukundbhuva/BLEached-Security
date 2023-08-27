import os
def notify_push_msg(i, text):
    def reset_push_paras():
        s_push_list.clear()
        s_push_max = 0
        s_push_cnt = 0

    def chk_text_byte_order(b_arr):
        if len(b_arr) > 2:
            is_little_endian = b_arr[0] == 255

            if not is_little_endian:
                b_arr[::2], b_arr[1::2] = b_arr[1::2], b_arr[::2]

        return b_arr

    def concat_byte_arrays(b_arr, b_arr2):
        b_arr3 = bytearray(len(b_arr) + len(b_arr2))
        b_arr3[:len(b_arr)] = b_arr
        b_arr3[len(b_arr):] = b_arr2
        return b_arr3

    s_push_list = []
    s_conn_seq = 0
    s_push_max = 0
    s_push_cnt = 0

    if len(text) > 48:
        text = text[:48]

    reset_push_paras()
    b_arr = bytearray([256 - 14])  # Two's complement representation of -14
    b_arr2 = bytes([i])
    b_arr3 = bytes([len(text)])
    b_arr4 = bytearray([0])
    b_arr5 = bytearray(16)

    i2 = 0
    while i2 < len(text):
        i3 = i2 + 8
        substring = text[i2:i3]

        try:
            chk_text_byte_order_result = chk_text_byte_order(substring.encode("utf-16"))
            b_arr5 = chk_text_byte_order_result[2:18] if len(chk_text_byte_order_result) >= 18 else chk_text_byte_order_result + bytes(16 - len(chk_text_byte_order_result))
        except UnicodeEncodeError:
            print("Unicode encoding error")

        s_push_list.append(concat_byte_arrays(b_arr, b_arr2 + b_arr3 + b_arr4 + b_arr5))
        b_arr4[0] = b_arr4[0] + 1
        i2 = i3

    if s_conn_seq == 0 and len(s_push_list) != 0:
        s_conn_seq = 41

    # Print the output in hexadecimal format using UTF-16 encoding
    for item in s_push_list:
        # hex_str = utf16_to_hex_string(item)
        # print(item.hex())
        os.system("gatttool --device=A4:C1:89:F9:11:08 --char-write-req --handle=0x0025 --value=" + item.hex())

i_value = 20
# text_value = "Mom: Test Mukund"
text_value = input("Enter Message: ")
# text_value = input("Call From: ")
notify_push_msg(i_value, text_value)
