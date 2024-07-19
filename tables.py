import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

# conn.execute('CREATE TABLE Users (Username VARCHAR(255),Email VARCHAR(255),Password VARCHAR(255),Type VARCHAR(255) DEFAULT "customer")')
# print("Created Users table successfully")

# conn.execute('INSERT INTO Users VALUES ("aditya123","anything@yahoo.com","123456","admin")')
# print("done")

# conn.execute('ALTER TABLE Users ADD Address VARCHAR(255)')
# print("alter 1 complete")

# conn.execute('ALTER TABLE Users ADD PhoneNo VARCHAR(255)')
# print("alter 2 complete")

# conn.execute('ALTER TABLE BuyShares RENAME COLUMN NetAssetvalue to NetAssetValue') 
# print("done")

#ALTER IN SQLITE3
# conn.execute('DROP TABLE BuyShares') 

# conn.execute('CREATE TABLE BuyShares (PortfolioId VARCHAR(255),CompanyName VARCHAR(255),SharesDescription VARCHAR(255),NetAssetValue DECIMAL(12,2),Units INT(10),Amount DECIMAL(12,2),date_buyshare DATE,Exchange DECIMAL(12,2))')
# print("Created BuyShares table successfully")

#ALTER IN SQLITE3
# conn.execute('DROP TABLE Companies') 

# conn.execute('CREATE TABLE Companies (CompanyId VARCHAR(255),CompanyName VARCHAR(255),CompanyAddress VARCHAR(255),CompanyPhoneNo VARCHAR(255),CompanyFaxNo VARCHAR(255),CompanyCity VARCHAR(255),CompanyProfile VARCHAR(255),CompanyTurnover DECIMAL(12,2),CompanyType VARCHAR(255),CompanyUsername VARCHAR(255),CompanyPassword VARCHAR(255))')
# print("Created Companies table successfully") 

#ALTER IN SQLITE3
# conn.execute('DROP TABLE Shares') 

# conn.execute('CREATE TABLE Shares (CompanyName VARCHAR(255),SharesId VARCHAR(255),CompanyType VARCHAR(255),SharesDescription VARCHAR(255),TotalShares INT(10),SharesSold INT(10),SharesLeft INT(10),StartNAV DECIMAL(12,2),date_share DATE)')
# print("Created Shares table successfully")

# conn.execute('DROP TABLE Users') 

# conn.execute('CREATE TABLE Users (UserId INTEGER PRIMARY KEY AUTOINCREMENT,Username VARCHAR(255),Email VARCHAR(255),Password VARCHAR(255),Type VARCHAR(255) DEFAULT "customer",Address VARCHAR(255),PhoneNo VARCHAR(255),Funds DECIMAL(12,2) DEFAULT 0)')
# print("Created Users table successfully")

# conn.execute('INSERT INTO Users(Username,Email,Password,Type) VALUES ("aditya123","anything@yahoo.com","123456","admin")')
# print("done")

# conn.execute('ALTER TABLE BuyShares ADD UserId INT(10)') 
# print("done")
 
# conn.execute('DELETE FROM BuyShares')

# conn.execute('CREATE TABLE Portfolio (PortfolioID INTEGER PRIMARY KEY AUTOINCREMENT, PANNo VARCHAR(255) , AccountNo VARCHAR(255) , BankName VARCHAR(255) , Branch VARCHAR(255), UserId INTEGER,FOREIGN KEY (UserId) REFERENCES Users(UserId))')

# conn.execute('DROP TABLE BuyShares') 
# conn.execute('CREATE TABLE BuyShares (PortfolioId VARCHAR(255),CompanyName VARCHAR(255),SharesId VARCHAR(255),NetAssetValue DECIMAL(12,2),Units INT(10),Amount DECIMAL(12,2),date_buyshare DATETIME,Exchange DECIMAL(12,2) DEFAULT 20,UserId INT(10))')
# print("Created BuyShares table successfully")


# conn.execute('DROP TABLE Inbox_user')
# conn.execute('CREATE TABLE Inbox_user (TID INT(10), Message VARCHAR(255) , UserId INTEGER,FOREIGN KEY (UserId) REFERENCES Users(UserId))')



# conn.execute('DROP TABLE Companies') 

# conn.execute('CREATE TABLE Companies (CompanyId VARCHAR(255),CompanyName VARCHAR(255),Symbol VARCHAR(255),CompanyAddress VARCHAR(255),CompanyPhoneNo VARCHAR(255),CompanyFaxNo VARCHAR(255),CompanyCity VARCHAR(255),CompanyProfile VARCHAR(255),CompanyTurnover DECIMAL(12,2),CompanyType VARCHAR(255),CompanyUsername VARCHAR(255),CompanyPassword VARCHAR(255))')
# print("Created Companies table successfully") 


conn.execute('DELETE FROM Inbox_user') 
# conn.execute('CREATE TABLE Inbox_user (Status VARCHAR(255), Message VARCHAR(255) , UserId INTEGER,FOREIGN KEY (UserId) REFERENCES Users(UserId))')
 
conn.commit()
print("Every task was completed")

conn.close()