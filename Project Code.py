import mysql.connector
from datetime import datetime, timedelta
from prettytable import PrettyTable



cnx = mysql.connector.connect(user='apartha4', password='200477042',
                              host='classdb2.csc.ncsu.edu', database='apartha4', port = 3306)

# Prints the Artists so User can see the IDs
def selectArtist():

    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "SELECT * FROM Artists"
    cursor.execute(query)

    # Fetch and print results
    print("\n")
    print("ArtistID", "ArtistName")
    for result in cursor.fetchall():
        print(result[0],"\t", result[1])
    
    print("\n")

    # Cursor Close
    cursor.close()

# Prints the Hosts so User can see the IDs
def selectHost():

    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "SELECT * FROM PodcastHosts"
    cursor.execute(query)

    # Fetch and print results
    print("\n")
    print("HostID", "Host Name")
    for result in cursor.fetchall():
        print(result[0],"\t", result[1])
    
    print("\n")

    # Cursor Close
    cursor.close()

# Prints the Labels so User can see the IDs
def selectLabel():

    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "SELECT * FROM RecordLabel"
    cursor.execute(query)

    # Fetch and print results
    print("\n")
    print("RLID", "Label Name")
    for result in cursor.fetchall():
        print(result[0],"\t", result[1])
    
    print("\n")

    # Cursor Close
    cursor.close()

# Insert a song into the database
def enterSong():
    try:
        
        # Begin the Transaction
        cnx.start_transaction()
        selectArtist()
        
        # Open the cursor
        cursor = cnx.cursor()

        # Enter the new song details
        print("Enter your song details:")
        title = input("Enter the song Title: ")
        releaseDate = input("Enter the song release date (YYYY-MM-DD): ")
        artistID = input("Enter the ArtistID from the above mentioned Artists: ")
        genres = input("Enter the Genre: ")
        royaltyRate = float(input("Enter the Royalty Rate(Enter True/False): "))
        royaltyPaid = bool(input("Enter whether the royalty is paid or not (True/False): "))
        releaseCountry = input("Enter the release country: ")
        language = input("Enter the language: ")
        duration  = float(input("Enter the duration: "))
        playcount = 0

        sql_query = """INSERT INTO Songs 
                    (Title, ReleaseDate, ArtistID, Genres, RoyaltyRate, RoyaltyPaid, ReleaseCountry, Language, Duration, Playcount) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (title, releaseDate, artistID, genres, royaltyRate, royaltyPaid, releaseCountry, language, duration, playcount)

        # Execute the query to insert a song into the database
        cursor.execute(sql_query, values)

        # Input the collaborated hosts of the song
        flag = int(input("Please enter 1 if there are any collaborated artists, else enter 0: "))
        while(flag):
            collab_artistID = int(input("Enter the collaborated artist ID: "))
            sql_query = """INSERT INTO CollaboratedBy VALUES(%s, %s, %s, %s)"""

            values = (collab_artistID, title, releaseDate, artistID)    
            cursor.execute(sql_query, values)

            flag = int(input("Please enter 1 if there are any collaborated artists, else enter 0: "))
        cnx.commit()

    except:

        # Rollback the changes if there are any issues
        print("There was an error, so the changes are rolled back")
        cnx.rollback()
    
    # Cursor Close
    cursor.close()

# Update the song given the song title, release date and artist id
def updateSong():

    selectArtist()
    
    # Open the cursor
    cursor = cnx.cursor()

    # Take user input for song title to update
    title = input("Enter the song title to update: ")
    releaseDate = input("Enter the release date of the song to update (YYYY-MM-DD) : ")
    artistID = int(input("Enter the correct artistID from the above given Artists: "))

    # Execute SQL query to select the record with the given song title
    sql_query = "SELECT * FROM Songs WHERE Title = %s and releaseDate = %s and ArtistID = %s"
    values = (title, releaseDate, artistID)
    cursor.execute(sql_query, values)

    # Fetch the record(s)
    result = cursor.fetchall()
    if not result:
        print("No record found with title: ", title)
    else:
        # Print the current data
        for row in result:
            print("Current data: ")
            print("Title: ", row[0])
            print("Release date: ", row[1])
            print("Artist ID: ", row[2])
            print("Genres: ", row[3])
            print("Royalty rate: ", row[4])
            print("Royalty paid: ", row[5])
            print("Release country: ", row[6])
            print("Language: ", row[7])
            print("Duration: ", row[8])
            print("Play count: ", row[9])

            # Take user input for new data
            print("Enter new values. Press enter to keep the current value.")
            new_title = input("Enter the new title: ") or row[0]
            new_release_date = input("Enter the new release date (YYYY-MM-DD): ") or row[1]
            new_artist_id = input("Enter the new artist ID: ") or row[2]
            new_genres = input("Enter the new genres: ") or row[3]
            try:
                new_royalty_rate = float(input("Enter the new royalty rate: ")) or row[4]
            except:
                new_royalty_rate = row[4]
            
            try:
                new_royalty_paid = bool(input("Enter whether the new royalty is paid or not (True/False): ")) or row[5]
            except:
                new_royalty_paid = row[5]

            new_release_country = input("Enter the new release country: ") or row[6]
            new_language = input("Enter the new language: ") or row[7]

            try:
                new_duration = float(input("Enter the new duration: ")) or row[8]
            except:
                new_duration = row[8]
            
            try:
                new_playcount = int(input("Enter the new playcount: ")) or row[9]
            except:
                new_playcount = row[9]

            # Execute SQL query to update the record with the new data
            sql_query = "UPDATE Songs SET Title = %s, ReleaseDate = %s, ArtistID = %s, Genres = %s, RoyaltyRate = %s, RoyaltyPaid = %s, ReleaseCountry = %s, Language = %s, Duration = %s, PlayCount = %s WHERE Title = %s and ReleaseDate = %s"
            values = (new_title, new_release_date, new_artist_id, new_genres, new_royalty_rate, new_royalty_paid, new_release_country, new_language, new_duration, new_playcount, title, releaseDate)
            cursor.execute(sql_query, values)

            cnx.commit()

            print(cursor.rowcount, "record(s) updated")
    
    # Close the cursor
    cursor.close()


# Delete the song given the song title, release date and artistID

def deleteSong():
    selectArtist()
    
    # Open the cursor
    cursor = cnx.cursor()

    # Take user input
    title = input("Enter the song title to delete: ")
    releaseDate = input("Enter the release date of the song to delete(YYYY-MM-DD): ")
    artistID = int(input("Enter the artistID: "))

    # Execute the query to delete a song
    sql_query = "DELETE FROM Songs WHERE Title = %s and releaseDate = %s and artistID = %s"
    values = (title, releaseDate, artistID)
    cursor.execute(sql_query, values)

    # Commit the changes and close the connection
    cnx.commit()
    print(cursor.rowcount, "record(s) deleted")
    cursor.close()


# Inputs the Artist information into the database
def enterArtist():

    # Opens the cursor
    cursor = cnx.cursor()

    # Getting the maximum ID of all the current artists
    cursor.execute("SELECT MAX(ArtistID) FROM Artists")
    max_id = cursor.fetchone()[0]

    # If there are no artists, set max_id to 2000
    if max_id is None:
        max_id = 2000

    # Increment the max_id by 1 to get the new ArtistID
    new_id = max_id + 1

    # Taking user input for new artist's details
    print("Enter the details of the Artist: ")
    name = input("Enter the name of the artist: ")
    primary_genre = input("Enter the primary genre of the artist (leave blank if unknown): ")
    country = input("Enter the country of the artist: ")
    type = input("Enter the type of the artist (solo, band, duo, etc.): ")
    status = input("Enter the status of the artist (active, inactive, retired, etc.): ")
    monthly_listeners = int(input("Enter the monthly listeners of the artist: "))

    # Inserting new artist into the table
    insert_query = """INSERT INTO Artists (ArtistID, Name, PrimaryGenre, Country, Type, Status, MonthlyListeners)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    insert_values = (new_id, name, primary_genre, country, type, status, monthly_listeners)

    cursor.execute(insert_query, insert_values)
    cnx.commit()

    # Close the connection
    cursor.close()
    print("New artist added successfully!")


# Deletes an artist given the artist ID
def deleteArtist():
    # get user input for artist ID to delete
    artist_id = int(input("Enter the ID of the artist you want to delete: "))

    # define the SQL query to delete the artist
    delete_query = "DELETE FROM Artists WHERE ArtistID = %s"

    # create a cursor object and execute the delete query with the artist ID parameter
    cursor = cnx.cursor()
    cursor.execute(delete_query, (artist_id,))

    # commit the changes to the database
    cnx.commit()

    print(cursor.rowcount,"record(s) deleted.")

    # close cursor
    cursor.close()


# Updates an artist given his ID
def updateArtist():
    cursor = cnx.cursor()

    # get the artist ID from user
    artist_id = input("Enter the artist ID you want to update: ")

    values = (artist_id,)
    # check if the artist ID exists in the database
    query = "SELECT * FROM Artists WHERE ArtistID = %s"
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result is None:
        print("Artist with ID" ,artist_id, "does not exist in the database.")
    else:
        # print current information of the artist
        print("Current Information:")
        print("ArtistID: ", result[0])
        print("Name: ", result[1])
        print("Primary Genre: ", result[2])
        print("Country: ", result[3])
        print("Type: ", result[4])
        print("Status: ", result[5])
        print("Monthly Listeners: ", result[6])
        
        # get new values for artist
        print("Enter new values. Press enter to keep the current value.")
        name = input("Artist Name: ") or result[1]
        genre = input("Primary Genre: ") or result[2]
        country = input("Artist Country: ") or result[3]
        artist_type = input("Type: ") or result[4]
        status = input("Status: ") or result[5]
        try:
            monthly_listeners = int(input("Monthly Listeners: ")) or result[6]
        except:
            monthly_listeners = result[6]
        

        # update artist information in the database
        query = "UPDATE Artists SET Name = %s, PrimaryGenre = %s, Country = %s, Type = %s, Status = %s, MonthlyListeners = %s WHERE ArtistID = %s"
        values = (name, genre, country, artist_type, status, monthly_listeners, artist_id)
        cursor.execute(query, values)
        cnx.commit()
        print(cursor.rowcount,"record(s) updated.")

    # close cursor
    cursor.close()


# Enter podcast host information into the database
def enterPodcastHost():
    cursor = cnx.cursor()

    # Get the current max HostID value from the table
    query = "SELECT MAX(HostID) FROM PodcastHosts"
    cursor.execute(query)
    result = cursor.fetchone()

    # Compute the new HostID value
    new_host_id = result[0] + 1 if result[0] else 6000

    # Prompt the user to enter the values for the new record
    print("Enter the Host details: ")
    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")
    phone = input("Enter the phone number: ")
    email = input("Enter the email address: ")
    city = input("Enter the city: ")

    # Insert a new record into the table
    insert_query = "INSERT INTO PodcastHosts (HostID, FirstName, LastName, Phone, Email, City) VALUES (%s, %s, %s, %s, %s, %s)"
    insert_values = (new_host_id, first_name, last_name, phone, email, city)
    cursor.execute(insert_query, insert_values)

    # Commit the transaction
    cnx.commit()

    # Close the cursor and connection
    cursor.close()

# Updates a host given his ID
def updateHost():

    # Opens the cursor and fetches the current host information
    cursor = cnx.cursor()
    host_id = input("Enter the HostID to update: ")
    cursor.execute("SELECT * FROM PodcastHosts WHERE HostID = %s", (host_id,))
    previous_info = cursor.fetchone()

    # Print the previous information
    print("Current information: ")
    print("First Name: ", previous_info[1])
    print("Last Name: ", previous_info[2])
    print("Phone Number: ", previous_info[3])
    print("Email: ", previous_info[4])
    print("City: ", previous_info[5])

    # User input for the new information
    print("Enter new values. Press enter to keep the current value.")
    new_first_name = input("Enter the new first name: ") or previous_info[1]
    new_last_name = input("Enter the new last name: ") or previous_info[2]
    new_phone = input("Enter the new phone number: ") or previous_info[3]
    new_email = input("Enter the new email address: ") or previous_info[4]
    new_city = input("Enter the new city: ") or previous_info[5]

    # Update the host's information
    cursor.execute("UPDATE PodcastHosts SET FirstName = %s, LastName = %s, Phone = %s, Email = %s, City = %s WHERE HostID = %s",
    (new_first_name, new_last_name, new_phone, new_email, new_city, host_id))

    print(cursor.rowcount,"record(s) updated.")

    # Commit the changes to the database and close the cursor
    cnx.commit()
    cursor.close()

# Delete a host given his ID
def deleteHost():
    # Opens a cursor
    cursor = cnx.cursor()

    # Executing query for the deleting a host
    host_id = input("Enter the HostID to delete: ")
    cursor.execute("DELETE FROM PodcastHosts WHERE HostID = %s", (host_id,))
    cnx.commit()
    print(cursor.rowcount,"record(s) deleted.")

    # Close the cursor
    cursor.close()

# Input data into the podcast
def enterPodcast():
    selectHost()

    # Open a cursor
    cursor = cnx.cursor()

    # Take input from user
    print("Enter Podcast details: ")
    host_id = input("Enter Podcast HostID: ")
    name = input("Enter Podcast Name: ")
    genres = input("Enter Genres: ")
    rating = float(input("Enter Rating: "))
    total_subscribers = int(input("Enter TotalSubscribers: "))
    language = input("Enter Language: ")
    episode_count = int(input("Enter EpisodeCount: "))
    sponsors = int(input("Enter Sponsors: "))

    # Insert values into the Podcast table
    sql = "INSERT INTO Podcast (HostID, Name, Genres, Rating, TotalSubscribers, Language, EpisodeCount, Sponsors) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (host_id, name, genres, rating, total_subscribers, language, episode_count, sponsors)
    cursor.execute(sql, val)

    # Commit changes to the database and close the cursor
    cnx.commit()
    cursor.close()

# Updates the podcast given the hostID and podcast name
def updatePodcast():

    selectHost()

    # Opens the cursor
    cursor = cnx.cursor()
    
    # Takes the user input
    host_id = input("Enter Podcast HostID: ")
    name = input("Enter Podcast Name: ")
    
    # Executes the information to get the current information about the podcast
    sql = "SELECT * FROM Podcast WHERE HostID = %s AND Name = %s"
    val = (host_id, name)
    cursor.execute(sql, val)
    result = cursor.fetchone()

    if result is None:
        print("Podcast not found.")
    else:
        # Print current information of the podcast
        print("Previous values: ")
        print("HostID: ", result[0])
        print("Podcast Name: ", result[1])
        print("Genres: ", result[2])
        print("Rating: ", result[3])
        print("Total Subscribers: ", result[4])
        print("Language: ", result[5])
        print("Episode Count: ", result[6])
        print("Sponsors: ", result[7])

        # Takes user input for the new values of the podcast
        print("Enter new values. Press enter to keep the current value.")
        new_host_id = input("Enter HostID: ") or result[0]
        new_name = input("Enter Name: ") or result[1]
        new_genre = input("Enter Genre: ") or result[2]
        try:
            new_rating = float(input("Enter new Rating: ")) or result[3]
        except:
            new_rating = result[3]
        
        try:
            new_subscribers = int(input("Enter new TotalSubscribers: ")) or result[4]
        except:
            new_subscribers = result[4]

        new_language = input("Enter new Language: ") or result[5]
        try:
            new_count = int(input("Enter new episode count: ")) or result[6]
        except:
            new_count = result[6]
        
        try:
            new_sponsor = int(input("Enter new sponsor count: ")) or result[7]
        except:
            new_sponsor = result[7]

        # Update values in the database
        sql = "UPDATE Podcast SET HostID = %s, Name = %s, Genres = %s, Rating = %s, TotalSubscribers = %s, Language = %s, EpisodeCount = %s, Sponsors = %s WHERE HostID = %s AND Name = %s"
        val = (new_host_id, new_name, new_genre, new_rating, new_subscribers, new_language, new_count, new_sponsor, result[0], result[1])
        cursor.execute(sql, val)

        # commit and close the cursor
        cnx.commit()
        cursor.close()
        print(cursor.rowcount, "record(s) updated.")


# Deletes the Podcast given the host ID and host name
def deletePodcast():

    selectHost()

    # Opens the cursor
    cursor = cnx.cursor()

    # Take user input for host id and name
    host_id = input("Enter HostID: ")
    name = input("Enter Podcast Name: ")

    # Execute the query for deleting the podcast
    sql = "DELETE FROM Podcast WHERE HostID = %s AND Name = %s"
    val = (host_id, name)
    cursor.execute(sql, val)

    print(cursor.rowcount,"record(s) deleted.")

    # Commit and close the cursor
    cnx.commit()
    cursor.close()


# Increase/ Decrease the episode count by 1 if new episode is added/deleted
def updateEpisodeCountBy1(host_id, podcast_name, val):
    # create a cursor object
    cursor = cnx.cursor()


    # Get the current episode count
    query = "SELECT EpisodeCount FROM Podcast WHERE HostID = %s AND Name = %s"
    params = (host_id, podcast_name)
    cursor.execute(query, params)
    result = cursor.fetchone()

    
    if result is not None:
    # Update the episode count
        episode_count = result[0] + val
        query = "UPDATE Podcast SET EpisodeCount = %s WHERE HostID = %s AND Name = %s"
        params = (episode_count, host_id, podcast_name)
        cursor.execute(query, params)
        cnx.commit()
        print(f"Episode count for {podcast_name} has been updated to {episode_count}")

    # close the cursor
    cursor.close()
    return result[0]+1

# Enter a new episode for a podcast
def enterPodcastEpisode():

    selectHost()

    # Opens the cursor
    cursor = cnx.cursor()

    # Take user input for each field
    print("Enter Podcast Episode details: ")
    host_id = int(input("Enter Host ID: "))
    podcast_name = input("Enter Podcast Name: ")
    episode_number = updateEpisodeCountBy1(host_id, podcast_name,1)
    episode_title = input("Enter Episode Title: ")
    duration = float(input("Enter Duration (in minutes): "))
    listening_count = int(input("Enter Listening Count: "))
    release_date = input("Enter Release Date (YYYY-MM-DD format): ")
    advertisement_count = int(input("Enter Advertisement Count: "))

    # Execute the query to enter the episode information
    data = (host_id, episode_number, podcast_name, episode_title, duration, listening_count, release_date, advertisement_count)
    sql = "INSERT INTO Episodes (HostID, EpisodeNumber, PodcastName, EpisodeTitle, Duration, ListeningCount, ReleaseDate, AdvertisementCount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, data)

    # Commit the changes and close the cursor
    cnx.commit()
    print(cursor.rowcount, "row(s) inserted.")
    cursor.close()

# Update the episode information given the episode number, hostID and podcast name
def updateEpisode():

    selectHost()

    # Open the cursor
    cursor = cnx.cursor()

    # Take the user input to enter the episode details
    host_id = input("Enter HostID: ")
    episode_number = input("Enter EpisodeNumber: ")
    podcast_name = input("Enter PodcastName: ")

    # Execute the select statement to show previous information
    query = "SELECT * FROM Episodes WHERE HostID = %s AND EpisodeNumber = %s AND PodcastName = %s"
    params = (host_id, episode_number, podcast_name)
    cursor.execute(query, params)
    result = cursor.fetchone()
    print("Current Episode Information: ")
    print("HostID: ", result[0])
    print("Episode Number: ", result[1])
    print("Podcast Name: ", result[2])
    print("Episode Title: ", result[3])
    print("Duration: ", result[4])
    print("ListeningCount: ", result[5])
    print("ReleaseDate: ", result[6])
    print("AdvertisementCount: ", result[7])

    # Take user input for the new episode information
    print("Enter new values. Press enter to keep the current value.")
    new_Episode_Title = input("Episode Title: ") or result[3]
    try:
        new_duration = float(input("Duration: ")) or result[4]
    except:
        new_duration = result[4]

    try:
        new_listening_count = int(input("Listening Count: ")) or result[5]
    except:
        new_listening_count = result[5]
    new_release_date = input("Release Date: ") or result[6]

    try:
        new_advertisement_count = int(input("Advertisement Count: ")) or result[7]
    except:
        new_advertisement_count = result[7]

    # Execute the query to update the episode with the new values
    sql_query = """
        UPDATE Episodes
        SET EpisodeTitle = %s, Duration = %s, ListeningCount = %s,
            ReleaseDate = %s, AdvertisementCount = %s
        WHERE HostID = %s AND EpisodeNumber = %s AND PodcastName = %s
    """
    data = (new_Episode_Title, new_duration, new_listening_count,
        new_release_date, new_advertisement_count, result[0], result[1], result[2])
    cursor.execute(sql_query, data)

    # Commit the changes and the close the cursor
    cnx.commit()
    print(cursor.rowcount, "row(s) updated.")
    cursor.close()


# Delete the episode details given the hostID, episode number and podcast name
def deleteEpisode():
    
    selectHost()

    # Open the cursor
    cursor = cnx.cursor()
    
    # Take user input for episode details
    host_id = input("Enter HostID: ")
    episode_number = input("Enter Episode Number: ")
    podcast_name = input("Enter Podcast Name: ")
    
    # Execute the query to delete the episode
    sql_query = """
            DELETE FROM Episodes
            WHERE HostID = %s AND EpisodeNumber = %s AND PodcastName = %s
        """
    
    # Reduce the episode count by 1, commit the database changes
    updateEpisodeCountBy1(host_id,podcast_name,-1)
    cursor.execute(sql_query,(host_id, episode_number, podcast_name))
    cnx.commit()

    # Close the cursor
    cursor.close()

# Input a new record label into the database
def enterLabel():
    cursor = cnx.cursor()

    # Get the maximum RLID value
    cursor.execute("SELECT MAX(RLID) FROM RecordLabel")
    max_rlid = cursor.fetchone()[0]

    # Increment the maximum RLID by one to get the new RLID value
    if max_rlid:
        rlid = max_rlid + 1 
    else:
        rlid = 3000
    # Prompt user for input
    print("Enter Record Label details: ")
    name = input("Enter Name: ")

    # Insert values into the RecordLabel table
    add_rl = ("INSERT INTO RecordLabel "
            "(RLID, Name) "
            "VALUES (%s, %s)")

    data_rl = (rlid, name)

    cursor.execute(add_rl, data_rl)

    # Commit changes to database and close the cursor
    cnx.commit()
    cursor.close()

# Update the record label given the RLID
def updateLabel():
    cursor = cnx.cursor()

    # Get input from user
    rlid = input("Enter the RLID of the RecordLabel you want to update: ")

    # Show the previous information of the Record Label
    query = "SELECT * from RecordLabel where RLID = %s"
    cursor.execute(query, (rlid,))
    oldName = cursor.fetchone()[1]
    print("Current Information: ")
    print("Label Name: ", oldName)
    print("Enter new values. Press enter to keep the current value.")
    new_name = input("Enter the new name for the RecordLabel: ") or oldName

    # Update the RecordLabel with the given RLID
    update_query = "UPDATE RecordLabel SET Name=%s WHERE RLID=%s"
    data = (new_name, rlid)
    cursor.execute(update_query, data)
    cnx.commit()
    print(cursor.rowcount, "row(s) updated.")

    # close the cursor
    cursor.close()

# Delete the record label given its ID
def deleteLabel():

    # Open the cursor
    cursor = cnx.cursor()

    # Get the RLID to be deleted from the user
    rlid = input("Enter RLID of RecordLabel to delete: ")

    # Deleting the RecordLabel with given RLID
    delete_query = "DELETE FROM RecordLabel WHERE RLID = %s"
    delete_data = (rlid,)
    cursor.execute(delete_query, delete_data)
    print(cursor.rowcount, "row(s) deleted.")
    cnx.commit()

    # Close the cursor
    cursor.close()

# Contract an artist to a Record Label
def contractedBy():

    selectArtist()
    selectLabel()

    # Open the cursor
    cursor = cnx.cursor()

    # Get user input for ArtistID and RLID
    artist_id = int(input("Enter ArtistID: "))
    rlid = int(input("Enter RLID: "))

    # Insert the data into the ContractedBy table
    add_contracted_by = ("INSERT INTO ContractedBy "
                        "(ArtistID, RLID) "
                        "VALUES (%s, %s)")

    data = (artist_id, rlid)
    cursor.execute(add_contracted_by, data)
    cnx.commit()

    # Close the cursor
    cursor.close()
    

# Enter values into an album
def enterAlbum():

    # Open the cursor
    cursor = cnx.cursor()

    try:
        cnx.start_transaction()
        # Check if the album exists
        album_name = input("Enter album name to check if it exists: ")
        cursor = cnx.cursor()
        query = "SELECT * FROM Album WHERE Name=%s"
        cursor.execute(query, (album_name,))
        result = cursor.fetchall()

        # If Album exists
        if len(result)!= 0:
            
            print("The album exists.")
            # Find the current maximum tracknumber
            query1 = ("""
                    SELECT MAX(TrackNumber) FROM Album WHERE Name = %s
                """)
            
            cursor.execute(query1, (album_name,))
            result1 = cursor.fetchone()
            maxTrackNumber = result1[0]

            # Keep adding the new songs 1 by 1 until not neccessary
            flag = int(input("Enter 1 if you want a song to be added else enter 0: "))
            while(flag):
                maxTrackNumber+=1

                # Take user input for song values
                title = input("Enter the song Title: ")
                releaseDate = input("Enter the song release date (YYYY-MM-DD): ")
                artistID = int(input("Enter the ArtistID: "))

                query = "INSERT INTO Album (Name, Title, ReleaseDate, ArtistID, ReleaseYear, Edition, TrackNumber) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                params = (album_name, title, releaseDate, artistID, result[4], result[5], maxTrackNumber)

                cursor.execute(query, params)
                flag = int(input("Enter 1 if you want a song to be added else enter 0: "))
            cnx.commit()

        
        # If album does not exist, create a new album
        else:
            print("Since old album does not exist, lets create a new one.")

            # Take user input for the album specific information
            release_year = int(input("Release year: "))
            edition = input("Edition: ")
            maxTrackNumber = 0

            # Keep adding the new songs 1 by 1 until not neccessary
            flag = int(input("Enter 1 if you want a song to be added else enter 0: "))
            
            while(flag):
                maxTrackNumber+=1

                # Take user input for song values
                title = input("Enter the song Title: ")
                releaseDate = input("Enter the song release date(YYYY-MM-DD): ")
                artistID = int(input("Enter the ArtistID: "))

                query = "INSERT INTO Album (Name, Title, ReleaseDate, ArtistID, ReleaseYear, Edition, TrackNumber) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                params = (album_name, title, releaseDate, artistID, release_year, edition, maxTrackNumber)
                cursor.execute(query, params)
                flag = int(input("Enter 1 if you want a song to be added else enter 0: "))

            cnx.commit()

    except:

        # Rollback the changes if there are any issues
        print("There was an error so the changes are rolled back")
        cnx.rollback()
    
    cursor.close()

# Update the only the play count for the songs
def updatePlayCount():

    # Open the cursor
    cursor = cnx.cursor()

    # Get user input for the song title
    song_title = input("Enter the title of the song: ")
    song_release_date = input("Enter the release date of the (YYYY-MM-DD): ")
    song_artist_id = int(input("Enter the song artist id for the song: "))

    new_play_count = int(input("Enter the new playcount for the mentioned song: "))

    # Execute SQL query to update the play count of the specified song
    update_query = "UPDATE Songs SET PlayCount = %s WHERE Title = %s and ReleaseDate = %s and ArtistID = %s"
    cursor.execute(update_query, (new_play_count, song_title, song_release_date, song_artist_id))

    print(cursor.rowcount, "record(s) updated")
    # Commit changes to the database and close the cursor
    cnx.commit()
    cursor.close()
    

# Update the monthly listeners for an Artist
def updateMonthlyListeners():
    cursor = cnx.cursor()

    # Get user input
    artist_id = int(input("Enter the ID of the artist: "))
    new_monthly_listeners = int(input("Enter the new monthly listeners value: "))

    # Execute SQL query to update the monthly listeners of the specified artist
    update_query = "UPDATE Artists SET MonthlyListeners = %s WHERE ArtistID = %s"
    cursor.execute(update_query, (new_monthly_listeners, artist_id))

    print(cursor.rowcount, "record(s) updated")

    # Commit changes to the database and close the cursor
    cnx.commit()
    cursor.close()



def totalSubscribersAndRatings():
    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    # Get user input for the podcast name and host id
    podcast_name = input("Enter the name of the podcast: ")
    host_id = int(input("Enter the host ID of the podcast: "))

    # Get user input for the new total subscribers and ratings values
    new_total_subscribers = int(input("Enter the new total subscribers value: "))
    new_ratings = float(input("Enter the new ratings value: "))

    # Execute SQL query to update the total subscribers and ratings of the specified podcast
    update_query = "UPDATE Podcast SET TotalSubscribers = %s, Rating = %s WHERE Name = %s AND HostID = %s"
    cursor.execute(update_query, (new_total_subscribers, new_ratings, podcast_name, host_id))

    print(cursor.rowcount, "record(s) updated")

    # Commit changes to the database and close the cursor
    cnx.commit()
    cursor.close()


# Update the listening count for an episode
def updateListeningCount():
    
    # Open the cursor
    cursor = cnx.cursor()
    
    # Take user input for the podcast episode
    podcast_name = input("Enter the podcast name: ")
    host_id = input("Enter the host ID: ")
    episode_number = input("Enter the episode number: ")

    # Take user input for the new values to be added
    new_count = input("Enter the new listening count: ")

    # Execute the query to update the listening count of the episode
    query = "UPDATE Episodes SET ListeningCount = %s WHERE PodcastName = %s AND HostID = %s AND EpisodeNumber = %s"
    params = (new_count, podcast_name, host_id, episode_number)
    cursor.execute(query, params)

    print(cursor.rowcount, "record(s) updated")

    # Commit the changes and close the cursor 
    cnx.commit()
    cnx.close()


# define a function to make payments to artists and record label for a song
def makePaymentForSongs():
    # Perform databse operations
    # create a cursor object to interact with the database
    cursor = cnx.cursor()

    # list of SQL queries to fetch data from the database
    querySong = "SELECT * FROM Songs" 
    querySongPayment = "SELECT * FROM SongPayment" 
    queryPaidTo = "SELECT * FROM PaidTo"
    queryFinance = "SELECT * FROM Finance"
    queryContractedBy = "SELECT * FROM ContractedBy"


    # execute the queries and store the results in variables
    cursor.execute(querySong)
    songs = cursor.fetchall()

    cursor.execute(querySongPayment)
    songPayment = cursor.fetchall()

    cursor.execute(queryPaidTo)
    paidTo = cursor.fetchall()

    cursor.execute(queryFinance)
    finance = cursor.fetchall()


    # finding maximum ID present in Finance to increment it while writing INSERT statement
    cursor.execute("SELECT MAX(PaymentID) FROM Finance")
    maxID = cursor.fetchone()[0]

    cursor.execute(queryContractedBy)
    contractedBy = cursor.fetchall()

    # prompt the user to enter the required details of the song for which the payment has to be made
    title = input("Enter song title: ")
    artist = int(input("Enter the main artist id: "))
    releaseDate = input("Enter release date (yyyy-mm-dd): ")
    # if we want to get the play count from the user for the current month
    # playCount = input("Enter play count for the song: ")
    month = input("Enter the month and year (yyyy-mm): ")
    
    # alternatively, the details can be hardcoded for testing purposes
    # title = "Electric Dreamscape"
    # artist = 2001
    # releaseDate = "2022-12-12"
    # #playCount = 10
    # month = "2023-04"

    # compare input given by user with Songs table to find the song's royalty rate
    for result in songs:

        if (title == result[0] and releaseDate == str(result[1]) and artist == result[2]):
                royaltyRate = result[4] # 5th column of Songs table is royalty rate
                playCount = result[-1] # last column of Songs table is play count of the current month

    # calculate the total amount, artist amount, and record label amount to be paid
    totalAmount = playCount * royaltyRate
    rlAmount = 0.3 * float(totalAmount)
    aAmount = 0.7 * float(totalAmount)

    # adding '01' as the date
    startDate = month + "-01"
    
    # calculate the end date for the payment period, which is one month after start date
    start_date = datetime.strptime(startDate, '%Y-%m-%d')

    next_month = start_date.replace(day=28) + timedelta(days=4)  # Add 4 days to get to next month
    end_date = next_month.replace(day=1)

    endDate = end_date.strftime('%Y-%m-%d')
    
    # get the corresponding record label ID of the artist from ContractedBy table
    for i in range(len(contractedBy)):
        if artist == contractedBy[i][0]:
            RLID = contractedBy[i][1]

    # insert the payment details into Finance, SongPayment, and PaidTo tables. The Payment ID
    # one more than the maximum of the PaymentID.
    queryInsert = f"INSERT INTO Finance VALUES({maxID+1}, 'SongPayment', {totalAmount})"
    cursor.execute(queryInsert) 

    queryInsertSP = f"INSERT INTO SongPayment VALUES({maxID+1}, '{startDate}', {playCount}, {totalAmount}, {rlAmount}, {aAmount}, '{endDate}')"
    cursor.execute(queryInsertSP)

    queryInsertPaidTo = f"INSERT INTO PaidTo VALUES('{title}', '{releaseDate}', {artist}, {RLID}, {maxID+1})"
    cursor.execute(queryInsertPaidTo)

    # commit the changes to the database
    cnx.commit()

    # close the cursor
    cursor.close()

# function to make payments to podcast hosts for their podcast episodes
def makePaymentForPodcasts():
    # create a cursor object to interact with the database
    cursor = cnx.cursor()

    # list of SQL queries to fetch data from the database
    queryEpisode = "SELECT * FROM Episodes"
    queryPodcastPayment = "SELECT * FROM PodcastPayment"
    queryPaidToPodcast = "SELECT * FROM PaidToPodcast"
    queryFinance = "SELECT * FROM Finance"
    queryCollaboratedHosts = "SELECT * FROM CollaboratedHosts"
    
    # execute each of the query and store the results fetched
    cursor.execute(queryEpisode)
    episodes = cursor.fetchall()

    cursor.execute(queryPodcastPayment)
    podcastPayment = cursor.fetchall()

    cursor.execute(queryPaidToPodcast)
    paidToPodcast = cursor.fetchall()

    cursor.execute(queryFinance)
    finance = cursor.fetchall()

     # finding maximum ID present in Finance to increment it while writing INSERT statement
    cursor.execute("SELECT MAX(PaymentID) FROM Finance")
    maxID = cursor.fetchone()[0]
    # new payment ID will be 1 more than the most recent payment ID
    newID = maxID + 1 

    cursor.execute(queryCollaboratedHosts)
    collaboratedHosts = cursor.fetchall()
    
    # hardcoded details for testing
    # host = 6001
    # podcast = 'Mind Over Matter: Exploring the Power of the Human Mind'
    # episode = 'Senses'
    # flatFee = 10
    # adRevenue = 2.5

    # prompt the user to enter details fo podcast episode to make payment
    host = int(input("Enter host ID: "))
    podcast = input("Enter podcast name: ")
    episodeNo = int(input("Enter episode number: "))
    flatFee = float(input("Enter fee per episode: "))
    adRevenue = float(input("Enter revenue per advertisement: "))
    
    # find the episode in the Episodes table that matches the input details and retrieve the advertisement count, release date, and episode number
    for result in episodes:
        if (host == result[0] and podcast == result[2] and episodeNo == result[1]):
            adCount = result[7]
            releaseDate = str(result[6])
            epNumber = result[1]

    # calculate the total payment amount based on the flat fee, ad count, and ad revenue
    totalAmount = flatFee + (adCount * adRevenue)

    # insert a new payment record into the Finance table with the new payment ID and payment type 'PodcastPayment'
    queryInsert = f"INSERT INTO Finance VALUES({newID}, 'PodcastPayment', {totalAmount})"
    cursor.execute(queryInsert) 

    # insert a new podcast payment record into the PodcastPayment table with the new payment ID, flat fee, total payment amount, and ad revenue
    queryInsertPP = f"INSERT INTO PodcastPayment VALUES({newID}, '{flatFee}', {totalAmount}, {adRevenue})"
    cursor.execute(queryInsertPP)

    # insert new record into the PaidToPodcast table with the host name, podcast, and episode number. 
    queryInsertPaidToPodcast = f"INSERT INTO PaidToPodcast VALUES({newID}, {host}, '{podcast}', {epNumber})"
    cursor.execute(queryInsertPaidToPodcast)
    
    #commit the changes to the database and close the cursor object
    cnx.commit()
    cursor.close()

def makeUserPayment():

    # create a cursor object to interact with the database
    cursor = cnx.cursor()
    
    # SQL queries to fetch data from the database
    queryUsers = "SELECT * FROM Users"
    cursor.execute(queryUsers)
    users = cursor.fetchall()

    # SQL query to find the most recent (maximum) payment ID
    cursor.execute("SELECT MAX(PaymentID) FROM Finance")
    maxID = cursor.fetchone()[0]
    # new ID is 1 more than maxID
    newID = maxID + 1

    # get user input for cycle date
    cycleDate = input("Enter payment cycle date(yyyy-mm-dd): ")

    # for all the users in the Users table, find their monthly subscription fee (result[7]) and add it to total amount
    # append the user ID to a list to be used later to insert into PayTo table
    totalAmount = 0
    idList = []
    for result in users:
        totalAmount += result[7]
        idList.append(result[0])

    # SQL query to insert data into Finance table with the new ID, payment type as 'User Payment', and the total amount received for that cycle date
    queryInsert = f"INSERT INTO Finance VALUES({newID}, 'UserPayment', {totalAmount})"
    cursor.execute(queryInsert) 
    
    # SQL Query to insert data into UserPayment table with new ID, cycle date, and the total amount
    queryInsertUP = f"INSERT INTO UserPayment VALUES({newID}, '{cycleDate}', {totalAmount})"
    cursor.execute(queryInsertUP)

    # to insert records into PayTo table with every payment from each of the user in that cycle
    # this table contains only the user ID and the corresponding payment ID
    for i in idList:    
        queryInsertPayTo = f"INSERT INTO PayTo VALUES({i}, {newID})"
        cursor.execute(queryInsertPayTo)

    #  #commit the changes to the database and close the cursor object
    cnx.commit()
    cursor.close()

def generateMonthlyPlayCountPerSong():
    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "Select Title, MonthlyPlayCount, StartDate, EndDate From SongPayment Natural Join PaidTo"
    cursor.execute(query)
    # Fetching Results and Printing Table
    t = PrettyTable(["Song Name", "Monthly Play Count", "Start Date", "End Date"])
    for result in cursor.fetchall():
        t.add_row([result[0], result[1], result[2], result[3]])
    print(t)
    cursor.close()


def generateMonthlyPlayCountPerAlbum():
    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "Select Name, StartDate, EndDate, SUM(MonthlyPlayCount) FROM SongPayment Natural Join PaidTo Natural Join Album Group BY Name, StartDate, EndDate;"
    cursor.execute(query)
    # Fetching Results and Printing Table
    t = PrettyTable(["Album Name", "Monthly Play Count", "StartDate", "EndDate"])
    for result in cursor.fetchall():
        t.add_row([result[0], result[3], result[1], result[2]])
    print(t)
    cursor.close()

def generateMonthlyPlayCountPerArtist():
    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "Select ArtistID,Name,StartDate, EndDate, SUM(MonthlyPlayCount) FROM SongPayment Natural JOIN PaidTo Natural JOIN Artists Group BY ArtistID,StartDate,EndDate;"
    cursor.execute(query)
    # Fetching Results and Printing Table
    t = PrettyTable(["Artist ID", "Artist Name", "Monthly Play Count", "Start Date", "End Date"])
    for result in cursor.fetchall():
        t.add_row([result[0], result[1], result[2], result[3], result[4]])
    print(t)
    cursor.close()

def getepisodesgivenpodcast():
    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "Select EpisodeTitle From Episodes Natural Join Podcast;"
    cursor.execute(query)
    # Fetching Results and Printing Table
    t = PrettyTable(["Episode Name"])
    for result in cursor.fetchall():
        t.add_row([result[0]])
    print(t)
    cursor.close()

def getsongssgivenalbum():
    # Getting Input
    name = str(input("Enter album name: "))
    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "SELECT Title, Name FROM Album WHERE Name = (%s);" % name
    cursor.execute(query)
    # Fetching Results and Printing Table
    t = PrettyTable(["Song Name", "Album Name"])
    for result in cursor.fetchall():
        t.add_row([result[0], result[1]])
    print(t)
    cursor.close()
    

def getsongssgivenartistID():
    # Getting Input
    artist_id = input("Enter the ArtistID: ")
    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "SELECT Title, ReleaseDate, ArtistID FROM Songs WHERE ArtistID = (%s);" % artist_id 
    cursor.execute(query)
    # Fetching Results and Printing Table
    t = PrettyTable(["Song Name", "Release Data", "Artist ID"])
    for result in cursor.fetchall():
        t.add_row([result[0], result[1], result[2]])
    print(t)
    cursor.close()

def podcastpaymentgiventimeline():
    # Getting Inputs
    host_id = input("Enter Host ID: ")
    start_date = input("Enter Start Date: ")
    end_date = input("Enter End Date: ")
    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "SELECT EpisodeNumber, PodcastName FROM Episodes WHERE HostID= (%s) AND ReleaseDate>= (%s) AND ReleaseDate<=(%s);"
    cursor.execute(query,(host_id, start_date, end_date))
    podcasts = []
    episodes = []
    for result in cursor.fetchall():
        podcasts.append(result[1])
        episodes.append(result[0])

    host_payment = 0
    for i in range(len(podcasts)):
        # Open the cursor and execute the query
        cursor = cnx.cursor()
        query = "SELECT PaymentID from PaidToPodcast WHERE Name = (%s) and EpisodeNumber = (%s);"
        cursor.execute(query, (podcasts[i], episodes[i]))
        for paymentID in cursor.fetchall():    
            cursor1 = cnx.cursor()
            query1 = "SELECT TotalPaymentForEpisode FROM PodcastPayment WHERE PaymentID = (%s);" % paymentID[0]
            cursor1.execute(query1)
            #host_payment+= float(cursor1.fetchall()[])
            p = (cursor1.fetchall())
            host_payment += (float(p[0][0]))
    print("The Payment made to the host is ", host_payment)

def paymentforartist():
    # Getting Inputs
    artist_id = input("Enter Artist ID: ")
    start_date = input("Enter Start Date: ")
    end_date = input("Enter End Date: ")
    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "SELECT Title, ReleaseDate, MainArtistID FROM CollaboratedBy WHERE ArtistID= (%s);" % artist_id
    cursor.execute(query)
    title, releasedate, mainartistid = [], [], []
    for result in cursor.fetchall():
        title.append(result[0])
        releasedate.append(result[1])
        mainartistid.append(result[2])

    paymentid = {}
    for i in range(len(title)):
        # Open the cursor and execute the query
        cursor = cnx.cursor()
        query = "SELECT PaymentID from PaidTo WHERE Title = (%s) AND ReleaseDate = (%s) AND ArtistID = (%s);"
        cursor.execute(query,(title[i], releasedate[i], mainartistid[i]))
        paymentid[i] = []
        for result in cursor.fetchall():
            paymentid[i].append(result[0])

    total_payment = {}
    for i in range(len(paymentid)):
        total_payment[i] = 0
        for val in range(len(paymentid[i])):
            # Open the cursor and execute the query
            cursor = cnx.cursor()
            
            query = "SELECT ArtistPayment FROM SongPayment WHERE PaymentID = (%s) AND StartDate >= (%s) AND EndDate <= (%s);"
            cursor.execute(query, (paymentid[i][val], start_date, end_date))
            for result in cursor.fetchall():
                total_payment[i]+=float(result[0])

    no_of_artists = []
    for i in range(len(title)):
        # Open the cursor and execute the query
        cursor = cnx.cursor()
        query = "SELECT count(*) FROM CollaboratedBy WHERE MainArtistID = (%s) AND ReleaseDate =(%s) AND Title = (%s);"
        cursor.execute(query,(mainartistid[i],releasedate[i], title[i]))
        for result in cursor.fetchall():
            no_of_artists.append(int(result[0])+1)
    collaborated_payment = 0
    for i in range(len(total_payment)):
        collaborated_payment += total_payment[i]/no_of_artists[i]

    mainartist_payment = 0
    song_unique_id = []
    payment_ids = []
    cursor = cnx.cursor()
    query = "SELECT Title, ReleaseDate, ArtistID, PaymentID FROM PaidTo WHERE ArtistID = (%s)" %artist_id
    # Open the cursor and execute the query
    cursor.execute(query)
    for result in cursor.fetchall():
        song_unique_id.append([result[0], result[1], result[2]])
        payment_ids.append(result[3])

    artist_payments = []
    main_paymentid = []
    for i in range(len(payment_ids)):
        # Open the cursor and execute the query
        cursor = cnx.cursor()
        query = "SELECT PaymentID, ArtistPayment FROM SongPayment WHERE PaymentID = (%s) AND StartDate >= (%s) AND EndDate <= (%s);"
        cursor.execute(query,(payment_ids[i], start_date,end_date))
        for result in cursor.fetchall():
            main_paymentid.append(result[0])
            artist_payments.append(result[1])

    payment_indices = []
    for i in main_paymentid:
        for j in range(len(payment_ids)):
            if payment_ids[j] == i:
                payment_indices.append(j)

    
    payment_count = 0
    main_artist_total_payment = 0
    for i in payment_indices:
        count = 1
        cursor = cnx.cursor()
        query = "SELECT count(*) FROM CollaboratedBy WHERE MainArtistID = (%s) AND ReleaseDate =(%s) AND Title = (%s);"
        cursor.execute(query,(song_unique_id[i][2],song_unique_id[i][1], song_unique_id[i][0]))
        try:
            for result in cursor.fetchall():
                count+=result[0]
        except:
            pass
        main_artist_total_payment += artist_payments[payment_count]/count
        payment_count+=1
    print("Total artist earning from ", start_date, " to ", end_date, "is ", float(collaborated_payment) + float(main_artist_total_payment))
    

def recordlabelpayment():
    # Getting Inputs
    rlid = input("Enter Record Label ID: ")
    start_date = input("Enter Start Date: ")
    end_date = input("Enter End Date: ")
    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "Select SUM(RecordLabelPayment), Name from SongPayment Natural Join PaidTo Natural Join RecordLabel WHERE StartDate >= (%s) AND EndDate <= (%s) GROUP BY RLID HAVING RLID = (%s);"
    cursor.execute(query,(start_date, end_date, rlid))
    ans = cursor.fetchall()[0]
    print("Earning from the Record Label", ans[1], "is", float(ans[0]))

def generatemonthlyrevenue():
    # Open the cursor and execute the query
    cursor = cnx.cursor()
    query = "select PaymentCycleDate, SUM(TotalEarnings) from UserPayment Group By(PaymentCycleDate);"
    cursor.execute(query)
    # Fetching Results and Printing Table
    t = PrettyTable(["Month", "Revenue"])
    for result in cursor.fetchall():
        t.add_row([result[0], result[1]])
    print(t)
    cursor.close()

def generateyearlyrevenue():
    # Open the cursor and execute the query
    cursor = cnx.cursor()
    t = PrettyTable(["Year", "Revenue"])
    query = " select EXTRACT(year from PaymentCycleDate), SUM(TotalEarnings) from UserPayment GROUP BY (EXTRACT(year from PaymentCycleDate));"
    cursor.execute(query)
    # Fetching Results and Printing Table
    for result in cursor.fetchall():
        t.add_row([result[0], result[1]])
    print(t)
    cursor.close()  


# Close the connection to the entire database
def connectionClose():
    try:
        cnx.close()
    except:
        exit()


def main():
    

    functionDict = {
        1: enterSong,
        2: updateSong,
        3: deleteSong,
        4: enterArtist,
        5: updateArtist,
        6: deleteArtist,
        7: enterPodcastHost,
        8: updateHost,
        9: deleteHost,
        10: enterPodcast,
        11: updatePodcast,
        12: deletePodcast,
        13: enterPodcastEpisode,
        14: updateEpisode,
        15: deleteEpisode,
        16: enterLabel,
        17: updateLabel,
        18: deleteLabel,
        19: contractedBy,
        20: enterAlbum,
        21: updatePlayCount,
        22: updateMonthlyListeners,
        23: totalSubscribersAndRatings,
        24: updateListeningCount,
        25: makePaymentForSongs,
        26: makePaymentForPodcasts,
        27: makeUserPayment
        28: generateMonthlyPlayCountPerSong

    }

    choicesList = ["1. Enter a song into the database.",
                   "2. Update a song in the database.",
                   "3. Delete a song in the database.",
                   "4. Enter an artist into the database.",
                   "5. Update an artist in the database.",
                   "6. Delete an artist in the database.",
                   "7. Enter a Podcast Host into the database.",
                   "8. Update a Podcast Host in the database.",
                   "9. Delete a Podcast Host in the database.",
                   "10. Enter a Podcast into the database.",
                   "11. Update a Podcast in the database.",
                   "12. Delete a Podcast in the database.", 
                   "13. Enter a Podcast Episode for a particular Podcast into the database.",
                   "14. Update a Podcast Episode in the database.",
                   "15. Delete a Podcast Episode in the database.", 
                   "16. Enter a Record Label into the database.",
                   "17. Update a Record Label in the database.",
                   "18. Delete a Record Label in the database.",
                   "19. Assign a label to an Artist.",
                   "20. Create/Update an Album.",
                   "21. Update the playcount for a song.",
                   "22. Update the monthly listeners for an artist.",
                   "23. Update the total subscribers and ratings for the Podcast",
                   "24. Update the listening count for an episode.",
                   "25. Make song payment.",
                   "26. Make Podcast Payment.",
                   "27. Make User Payment.",
                   "28. Generate Monthly PlayCount Per Song"

                   ]
    
    for cho in choicesList:
        print(cho)
    choice = int(input("Enter a choice from the above given options(If any other option is entered the code would exit): "))
    while(choice>0 and choice<=len(choicesList)):
        functionDict[choice]()
        for cho in choicesList:
            print(cho)
        choice = int(input("Enter a choice from the above given options(If any other option is entered the code would exit): "))

    connectionClose()


if __name__ == "__main__":
    main()
