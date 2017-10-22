import sqlite3

""" Problems Functions """

def add_problem(subject, question, answer, conn):
    # create a cursor to database conn
    c = conn.cursor()
    
    # Insert a row of data
    c.execute("INSERT INTO problems (subject,question,answer) VALUES ('" +
              subject + "','" + question + "','" + answer + "')")
    
    # Save (commit) the changes
    conn.commit()  

def remove_problem(qid, conn):
    c = conn.cursor()
    # Deletes a row of data
    c.execute("DELETE FROM problems WHERE id = " + str(qid))
    conn.commit()

def update_problem_question(qid, new_question, conn):
    c = conn.cursor()
    # Updates a question
    c.execute("UPDATE problems SET question = '" + new_question +
              "' WHERE id = " + str(qid))
    conn.commit()

def update_problem_answer(qid, new_ans, conn):
    c = conn.cursor()
    # Updates an answer
    c.execute("UPDATE problems SET answer = '" + new_ans +
              "' WHERE id = " + str(qid))
    conn.commit()

def update_problem_subject(qid, new_sub, conn):
    c = conn.cursor()
    # Updates a subject
    c.execute("UPDATE problems SET subject = '" + new_sub +
              "' WHERE id = " + str(qid))
    conn.commit()
    
""" Users Functions """   

def add_user(role, name, email, password, conn):
    # create a cursor to database conn
    c = conn.cursor()
    
    # Insert a row of data
    c.execute("INSERT INTO users (role,name,email,password) VALUES ('" +
              role + "','" + name + "','" + email + "','" + password + "')")
    
    # Save (commit) the changes
    conn.commit()
    
def remove_user(uid, conn):
    c = conn.cursor()
    # Deletes a row of data
    c.execute("DELETE FROM users WHERE id = " + str(uid))
    conn.commit()
    
def update_user_role(uid, new_role, conn):
    c = conn.cursor()
    # Updates a question
    c.execute("UPDATE users SET role = '" + new_role +
              "' WHERE id = " + str(uid))
    conn.commit()    

def update_user_name(uid, new_name, conn):
    c = conn.cursor()
    # Updates a question
    c.execute("UPDATE users SET name = '" + new_name +
              "' WHERE id = " + str(uid))
    conn.commit()

def update_user_email(uid, new_email, conn):
    c = conn.cursor()
    # Updates an answer
    c.execute("UPDATE users SET email = '" + new_email +
              "' WHERE id = " + str(uid))
    conn.commit()

def update_user_password(uid, new_sub, conn):
    c = conn.cursor()
    # Updates a subject
    c.execute("UPDATE users SET password = '" + new_password +
              "' WHERE id = " + str(uid))
    conn.commit()    