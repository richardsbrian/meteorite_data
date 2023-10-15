from make_gif import make_gif
from maps import make_world_map, make_americas_map
from combine_data_to_pdf import make_pdf
from charts import most_common_types, number_of_strikes_on_continents


def make_data_chart_pdf():
    print("+++++    Working...  +++++")

    make_world_map()
    make_americas_map()
    most_common_types()
    number_of_strikes_on_continents()
    make_pdf()

    print("+++++    PDF Complete    +++++")


def make_strike_gif():
    print("Creating a GIF. This might take some time. Do you want to proceed? (yes/no)")
    user_input = input()

    if user_input.lower() == "no":
        print("GIF creation canceled.")
        return

    print("+++++    Working...  +++++")

    make_gif()

    print("+++++    GIF Creation Complete    +++++")


def main():
    while True:
        print("Options:")
        print("1. Make Data Charts")
        print("2. Make GIF")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            make_data_chart_pdf()
        elif choice == "2":
            make_strike_gif()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
