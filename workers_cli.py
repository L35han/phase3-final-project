import argparse
from models import create_connection, Worker

def main():
    parser = argparse.ArgumentParser(description="Worker Management System")
    subparsers = parser.add_subparsers(dest="command")

    add_worker_parser = subparsers.add_parser("add", help="Add a worker")
    add_worker_parser.add_argument("name", help="Worker name")
    add_worker_parser.add_argument("age", type=int, help="Worker age")
    add_worker_parser.add_argument("email", help="Worker email")

    delete_worker_parser = subparsers.add_parser("delete", help="Delete a worker")
    delete_worker_parser.add_argument("worker_id", type=int, help="Worker ID")

    list_workers_parser = subparsers.add_parser("list", help="List all workers")

    view_worker_parser = subparsers.add_parser("view", help="View a worker")
    view_worker_parser.add_argument("worker_id", type=int, help="Worker ID")

    find_worker_parser = subparsers.add_parser("find", help="Find a worker by name")
    find_worker_parser.add_argument("name", help="Worker name")

    args = parser.parse_args()

    conn = create_connection()
    if conn is not None:
        if args.command == "add":
            worker = Worker(args.name, args.age, args.email)
            worker.save_to_db(conn)
            print(f"Worker added with ID {worker.id}")
        elif args.command == "delete":
            worker = Worker.find_by_id(conn, args.worker_id)
            if worker is not None:
                worker.delete_from_db(conn)
                print("Worker deleted")
            else:
                print("Worker not found")
        elif args.command == "list":
            workers = Worker.get_all(conn)
            for worker in workers:
                print(worker)
        elif args.command == "view":
            worker = Worker.find_by_id(conn, args.worker_id)
            if worker is not None:
                print(worker)
            else:
                print("Worker not found")
        elif args.command == "find":
            worker = Worker.find_by_name(conn, args.name)
            if worker is not None:
                print(worker)
            else:
                print("Worker not found")

if __name__ == "__main__":
    main()
    