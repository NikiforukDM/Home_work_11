from AddressBook_11 import AddressBook, Record, Name, Phone, Field, Birthday


def parser_commands(command: str):
    command = command.strip().lower().split(' ')
    return command


if __name__ == '__main__':
    book = AddressBook()
    print('Commands: add contact(+name+-number+-date), add phone(+name+number),add birthday (+name+date),\n'
          'show book, days to birthday(+name) , change phone(+2 numbers), delete phone(+ number)')

    while True:
        command = parser_commands(input('Enter your command:'))
        if len(command) == 3 and ' '.join(command[0:2]) == 'add contact':
            book.add_contact(
                name=Name(value=command[2]))
        elif len(command) == 5 and ' '.join(command[0:2]) == 'add contact':
            book.add_contact(
                name=Name(value=command[2]), phone=Phone(value=command[3]), birthday=Birthday(value=command[4]))
        elif len(command) == 4:
            if ' '.join(command[0:2]) == 'add contact':
                book.add_contact(
                    name=Name(value=command[2]), phone=Phone(value=command[3]))

            elif ' '.join(command[0:2]) == 'add phone':
                a = Record(name=Name(value=command[2]))
                if a.name.value in book:
                    book.get(
                        Record(name=Name(value=command[2])).name.value).add_phone(Phone(value=command[3]))
                else:
                    print(f'Name {command[2]} does not exist')
            elif ' '.join(command[0:2]) == 'change phone':
                a = Record(name=Name(value=command[2]))
                if a.name.value in book:
                    try:
                        book.get(
                            Record(name=Name(value=command[2])).name.value).change_phone(command[3], Phone(value=command[4]))
                    except IndexError:
                        print('Enter two numbers, not one')
            elif ' '.join(command[0:2]) == 'delete phone':
                a = Record(name=Name(value=command[2]))
                if a.name.value in book:
                    book.get(
                        Record(name=Name(value=command[2])).name.value).delete_phone(command[3])

            elif ' '.join(command[0:2]) == 'add birthday':
                a = Record(name=Name(value=command[2]))
                if a.name.value in book:
                    book.get(
                        Record(name=Name(value=command[2])).name.value).add_birthday(Birthday(value=command[3]))
                else:
                    print(f'Name {command[2]} does not exist')

            elif ' '.join(command[0:3]) == 'days to birthday':

                a = Record(name=Name(value=command[3]))
                if a.name.value in book:
                    book.get(
                        Record(name=Name(value=command[3])).name.value).days_to_birthday()
                else:
                    print(f'Name {command[3]} does not exist')

        elif len(command) == 2 and ' '.join(command[0:2]) == 'show book':
            print(next(book))

        else:
            print('Entered string is not correct')
        print(book)
