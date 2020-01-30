import psycopg2
import sys

def updateRepoUser(repo_name, repo_host):
    try:
        connection = psycopg2.connect(user = "[my username]",
                                      password = "[my password]",
                                      host = repo_host,
                                      port = "5432",
                                      database = "[my database]")

        cursor = connection.cursor()

        username = sys.argv[1]

        # Set status to 1 if argument not passed. Otherwise, set it to argument
        status = 1 if len(sys.argv) < 3 else sys.argv[2]

        # Show record before update.
        select_query = """SELECT email, status FROM auth WHERE username = %(username)s"""
        cursor.execute(select_query, {'username': username})
        record = cursor.fetchone()
        print(record)

        # Update record.
        sql_update_query = """Update auth SET status = %(status)s where username = %(username)s"""
        cursor.execute(sql_update_query, {'status': status, 'username': username})
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully")

        # Show record after update.
        sql_select_query = """SELECT email, status FROM auth WHERE username = %(username)s"""
        cursor.execute(sql_select_query, {'username': username})
        record = cursor.fetchone()
        print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print(repo_name + " PostgreSQL connection is closed")
            print("\n")

# Repositories to update
repos = {"apt": "[ip address or host]", "containers": "[ip address or host]", "yum": "[ip address or host]"}

# Loop through and run above function through the repositories dictionary.
for repo, host in repos.items():
    updateRepoUser(repo, host)