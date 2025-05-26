import sys

clients = [
    'andrew@gmail.com',
    'jessica@gmail.com',
    'ted@mosby.com',
    'john@snow.is',
    'bill_gates@live.com',
    'mark@facebook.com',
    'elon@paypal.com',
    'jessica@gmail.com'
    ]

participants = [
    'walter@heisenberg.com',
    'vasily@mail.ru',
    'pinkman@yo.org',
    'jessica@gmail.com',
    'elon@paypal.com',
    'pinkman@yo.org',
    'mr@robot.gov',
    'eleven@yahoo.com'
    ]

recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

def call_center_task():
    #Return clients who haven't seen the promotional email
    clients_set = set(clients)
    recipients_set = set(recipients)
    return list(clients_set - recipients_set)

def potential_clients_task():
    #Return participants who are not clients
    clients_set = set(clients)
    participants_set = set(participants)
    return list(participants_set - clients_set)

def loyalty_program_task():
    #Return clients who didn't participate in the event
    clients_set = set(clients)
    participants_set = set(participants)
    return list(clients_set - participants_set)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <task_name>")
        print("Available tasks: call_center, potential_clients, loyalty_program")
        return
    
    task = sys.argv[1]
    
    if task == 'call_center':
        result = call_center_task()
        print("Clients who haven't seen the promotional email:")
    elif task == 'potential_clients':
        result = potential_clients_task()
        print("Participants who are not clients:")
    elif task == 'loyalty_program':
        result = loyalty_program_task()
        print("Clients who didn't participate in the event:")
    else:
        raise ValueError("Invalid task name. Available tasks: call_center, potential_clients, loyalty_program")
    
    for email in result:
        print(email)

if __name__ == "__main__":
    main()