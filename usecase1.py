import psycopg2 

# Establish connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="vishal69",
    host="localhost",
    port="5432"
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

try:
    # Read the error_message column from the deployment_history table
    cur.execute("SELECT id, errors_message FROM deployment_detailhistory")

    # Fetch all rows from the query result
    rows = cur.fetchall()

    for row in rows:
        id,errors_message = row

        # Check if error_message is not None
        if errors_message is not None and "ERROR 1064(42000)" in errors_message:
            # Update the specified columns based on the condition
            cur.execute("""
                UPDATE deployment_detailhistory 
                SET 
                    failure_category = %s,
                    prevention_plan = %s,
                    resolution = %s,
                    reason = %s,
                    auto_analyzed = %s
                WHERE id = %s
            """, ("user sql error", "Improve communication to users if it's a user error","Improve communication to users if it's a user error","Link doesn't work but after checking error message user error (syntax)","YES",id))
        elif errors_message is not None and "ERROR 1054(42S22)" in errors_message:
            cur.execute("""
                UPDATE deployment_detailhistory 
                SET 
                    failure_category = %s,
                    prevention_plan = %s,
                    resolution = %s,
                    reason = %s,
                    auto_analyzed = %s
                WHERE id = %s
            """, ("user sql error", "Improve communication to users if it's a user error","Improve communication to users if it's a user error","Link doesn't work but after checking error message user error (syntax)","YES",id))
        elif errors_message is not None and "ERROR: Error fetching remote repo origin" in errors_message:
            cur.execute("""
                UPDATE deployment_detailhistory 
                SET 
                    failure_category = %s,
                    prevention_plan = %s,
                    resolution = %s,
                    reason = %s,
                    auto_analyzed = %s
                WHERE id = %s
            """, ("User error", "Correction in the branch name&nbsp","Correction in the branch name&nbsp","Incorrect branch name given by user","YES",id))
        elif errors_message is not None and "ERROR 1050 (42S01)" in errors_message:
            cur.execute("""
                UPDATE deployment_detailhistory 
                SET 
                    failure_category = %s,
                    prevention_plan = %s,
                    resolution = %s,
                    reason = %s,
                    auto_analyzed = %s
                WHERE id = %s
            """, ("Incorrect SQL query", "Execute this in lower environment first by taking prod DB backup","updated sql and reran the job","Need to modify sql to avoid creating same table again; please add if table exists conditions","YES",id))
        elif errors_message is not None and "ERROR 1146 (42S02)" in errors_message:
            cur.execute("""
                UPDATE deployment_detailhistory 
                SET 
                    failure_category = %s,
                    prevention_plan = %s,
                    resolution = %s,
                    reason = %s,
                    auto_analyzed = %s
                WHERE id = %s
            """, ("Incorrect SQL query", "<p>Improve communication to users&nbsp;</p>","<p>Improve communication to users&nbsp;</p>","<p>Incorrect SQL query</p>","YES",id))
        elif errors_message is not None and "ERROR: script returned exit code 1" in errors_message:
            cur.execute("""
                UPDATE deployment_detailhistory 
                SET 
                    failure_category = %s,
                    prevention_plan = %s,
                    resolution = %s,
                    reason = %s,
                    auto_analyzed = %s
                WHERE id = %s
            """, ("Missing failure category", "<p>Please update pipelines whenever K8s secrets and GIT credentials are updated</p>","k8s secret & git-creds has  been updated","<E0324 09:09:23.142019      12 main.go:535] ''msg''=''too many failures, aborting'' ''error''=''Run(git clone -v --no-checkout -b master --depth 1 git@github.com:Chrome-River/configuration.git /opt/scripts): exit status 128: { stdout: '', stderr: ''Cloning into  /opt/scripts @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ @       WARNING: POSSIBLE DNS SPOOFING DETECTED!          @ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ The RSA host key for github.com has changed, and the key for the corresponding IP address 192.30.255.113 is unknown. This could either mean that DNS SPOOFING is happening or the IP address for the host and its host key have changed at the same time. @@@@@@@@@@@@@@@@","YES",id))
    conn.commit()
    print("Changes saved successfully.")

except psycopg2.Error as e:
    print("Error:", e)

finally:
    # Close the cursor and connection
    cur.close()
    conn.close()
