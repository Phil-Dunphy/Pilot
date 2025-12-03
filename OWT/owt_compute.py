import random
import roundClock
import squareClock
import combine_images
farben = ["light", "dark"]
formen = ["rund", "eckig"]
def generate_3x3():
    kritische_elemente = farben + formen

    kritisches_element = random.choice(kritische_elemente)
    print("kritisches Element:", kritisches_element)

    elemente = []

    if kritisches_element in farben:
        # kritische Eigenschaft ist die Farbe
        krit_farbe = kritisches_element
        andere_farbe = [f for f in farben if f != krit_farbe][0]

        # 4 Elemente mit kritischer Farbe
        elemente += [[krit_farbe, random.choice(formen)] for _ in range(4)]
        # 5 Elemente mit anderer Farbe
        elemente += [[andere_farbe, random.choice(formen)] for _ in range(5)]

    elif kritisches_element in formen:
        # kritische Eigenschaft ist die Form
        krit_form = kritisches_element
        andere_form = [f for f in formen if f != krit_form][0]

        # 4 Elemente mit kritischer Form
        elemente += [[random.choice(farben), krit_form] for _ in range(4)]
        # 5 Elemente mit anderer Form
        elemente += [[random.choice(farben), andere_form] for _ in range(5)]

    else:
        raise ValueError("Unbekanntes kritisches Element")

    # Falls du die Reihenfolge mischen willst:



    start_number = random.randint(1,8)
    elm_number = 1
    pointers = []
    for i in elemente:
        farbe = i[0]
        form = i[1]
        pointer = random.randint(0,7)

        clockR = roundClock.RoundClock()
        clockS =  squareClock.SquareClock()

        if form == "rund":
            clockR.generate_clock(
                start_number=start_number,
                visible_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
                pointer_position=pointer,
                output_file=f"images/clock_{elm_number}.png",
                theme=farbe

            )
            pointers.append(pointer)
        elif form == "eckig":

            clockS.generate_clock(
            start_number=start_number,
            visible_numbers=[1,5],  # Show all numbers
            pointer_position=pointer,
            output_file=f"images/clock_{elm_number}.png",
            theme=farbe,
        )
            pointers.append(pointer )
        elm_number +=1


    pointers_bereinigt = [((p + start_number - 1) % 8) + 1 for p in pointers]
    elements = list(range(9))
    random.shuffle(elements)


    korrekte_values = [pointers_bereinigt[i] for i in elements if i <= 3]
    print("Korrekt:", korrekte_values)


    combine_images.combine_images(elements)

def generate_einzeln():
    form = "rund"
    farbe = "dark"
    start_number = 0
    pointer = 0
    visible_numbers= [1, 2, 3, 4, 5, 6, 7, 8],
    file_name = "images/clock_single.png"

    clockR = roundClock.RoundClock()
    clockS = squareClock.SquareClock()

    if form == "rund":
        clockR.generate_clock(
            start_number=start_number,
            visible_numbers=visible_numbers,
            pointer_position=pointer,
            output_file=file_name,
            theme=farbe

        )
    elif form == "eckig":

        clockS.generate_clock(
            start_number=start_number,
            visible_numbers=visible_numbers,
            pointer_position=pointer,
            ouutput_file=file_name,
            theme=farbe,
        )


generate_einzeln()
generate_3x3()