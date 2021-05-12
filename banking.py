from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

import os
import logging
'''
SQLAlchemy ORM code adapted from https://docs.sqlalchemy.org/en/14/orm/tutorial.html
'''

# logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
#:: %(message)s', level=logging.INFO, filename='banking.log')
mylogs = logging.getLogger(__name__)
mylogs.setLevel(logging.DEBUG)
file = logging.FileHandler('banking.log')
file.setLevel(logging.INFO)
fileformat = logging.Formatter(
    "%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S")
file.setFormatter(fileformat)
mylogs.addHandler(file)
db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(file)
db_logger.setLevel(logging.INFO)


Base = declarative_base()
base_file_path = os.path.dirname(os.path.abspath(__file__))
helper_folder = 'banking'
SQLITE_DB = 'banking.sqlite'
full_db_name = f'{base_file_path}/{helper_folder}/{SQLITE_DB}'
db_string = f'sqlite:///{full_db_name}'
engine = create_engine(db_string, echo=False)
Session = sessionmaker(bind=engine)


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    street_address = Column(String)
    city = Column(String)
    zip = Column(String)
    phone = Column(String)
    email = Column(String)

    def __repr__(self):
        return "<Customer(last_name='%s', first_name='%s', middle_name='%s', street_address='%s', city='%s', zip='%s', phone='%s', email='%s')>" % (
            self.last_name, self.first_name, self.middle_name, self.street_address, self.city, self.zip, self.phone, self.email)

    def full_name(self):
        '''      
        Returns full name for the customer

        Parameters: 
            None

        Returns:
            First, Middle, Last names of the customer separated by spaces.
        '''
        return f'{self.first_name} {self.middle_name} {self.last_name}'


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    balance = Column(Integer)

    def __repr__(self):
        return "<Account(type='%s', customer_id = '%s', balance='%s')>" % (
            self.type, self.customer_id, self.balance)

    def format_balance(self):
        '''      
        Converts balance from an integer (*100) to a float. Balances are stored as integers.

        Parameters: 
            None

        Returns:
            Floating point representation of balance.
        '''
        return float(self.balance)/100

    def withdrawal(self, amount):
        '''      
        Processes withdrawal operation from the account

        Parameters: 
            Amount to withdrawal

        Returns:
            Balance after withdrawal
        '''
        if self.balance == None:
            self.balance = amount * -100
        else:
            self.balance = self.balance - int(amount * 100)
        return self.format_balance()

    def deposit(self, amount):
        '''      
        Processes deposit operation into the account

        Parameters: 
            Amount to desposit

        Returns:
            Balance after deposit
        '''
        if self.balance == None:
            self.balance = amount * 100
        else:
            self.balance = self.balance + int(amount * 100)
        return self.format_balance()


def init_data():
    '''      
    Initialize the database and insert some starter data.

    Parameters: 
        None

    Returns:
        None
    '''
    if os.path.exists(full_db_name):
        os.unlink(full_db_name)

    Base.metadata.create_all(engine)

    with Session() as session:
        session.add_all([
            Customer(last_name='Person', first_name='Jason', middle_name='Scott',
                     street_address='105 N. Main', city='Longview', zip='73112', phone='555-123-4567', email='jason@spam.com'),
            Customer(last_name='Person', first_name='Harper', middle_name='Jane',
                     street_address='106 N. Main', city='Longview', zip='73112', phone='555-765-4321', email='harper@spam.com')])
        session.commit()


def print_menu():
    print(' ____________________________________')
    print('| 0 - End Session                    |')
    print('| 1 - List Customers                 |')
    print('| 2 - Set Current Customer           |')
    print('| 3 - Deposit                        |')
    print('| 4 - Withdrawal                     |')
    print('|____________________________________|')


def main():
    with Session() as session:
        choice = ''
        while choice != '0':
            print_menu()
            choice = input('Select option: ')
            if choice == '1':
                for instance in session.query(Customer).order_by(Customer.id):
                    print(f'{instance.id} {instance.full_name()}')
            if choice == '2':
                current_customer = input('Enter customer id: ')
                # session.query(Account).filter_by(id=int(current_customer)).first()
                current_account = Account(id=int(current_customer))
            if choice == '3':
                amount = input('Enter deposit amount: ')
                new_balance = current_account.deposit(float(amount))
                print(f'New Balance: {new_balance}')
            if choice == '4':
                amount = input('Enter withdrawal amount: ')
                new_balance = current_account.withdrawal(float(amount))
                print(f'New Balance: {new_balance}')
        session.commit()


if __name__ == '__main__':
    init_data()
    main()
