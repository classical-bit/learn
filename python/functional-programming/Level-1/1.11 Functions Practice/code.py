def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    r = int(hex_color[:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:], 16)

    return r, g, b

def is_hexadecimal(hex_string: str) -> bool:
    try:
        int(hex_string, 16)
        return True
    except Exception:
        return False

string = "A020F0"

if is_hexadecimal(string):
    red_value, green_value, blue_value = hex_to_rgb(string)
    print(red_value) # 160
    print(green_value) # 32
    print(blue_value) # 240
else:
    print("Incorrect hex string passed!")
