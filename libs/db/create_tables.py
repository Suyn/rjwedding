from libs.db.connect import engine, Base


def run():
    print("Create start......")
    Base.metadata.create_all(engine)
    print("Successful!")

if __name__ == '__main__':
    run()
