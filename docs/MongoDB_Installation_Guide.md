# Installation Guide for MongoDB and MongoDB Compass

This comprehensive guide will walk you through the step-by-step process of installing MongoDB and MongoDB Compass on Windows with screenshots.

## Table of Contents
1. [MongoDB Installation](#mongodb-installation)
2. [MongoDB Compass Installation](#mongodb-compass-installation)
3. [Connecting MongoDB Compass to MongoDB](#connecting-mongodb-compass-to-mongodb)

## MongoDB Installation

### Step 1: Download MongoDB Installer
1. Visit the MongoDB Download Center: [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
2. Select the following options:
   - Version: Select the latest version (currently 8.0)
   - Platform: Windows
   - Package: MSI
3. Click the "Download" button

![MongoDB Download Page](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/1.png)

### Step 2: Run the MongoDB Installer
1. Locate the downloaded .msi file and double-click to run it
2. Click "Next" on the welcome screen

![MongoDB Installation Welcome Screen](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/2.png)

### Step 3: Accept License Agreement
1. Read the End-User License Agreement
2. Check "I accept the terms in the License Agreement"
3. Click "Next"

![MongoDB License Agreement](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/3.png)

### Step 4: Choose Setup Type
1. Select "Complete" for a full installation
2. Click "Next"

![MongoDB Setup Type](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/4.png)

### Step 5: Service Configuration
1. Check "Install MongoDB as a Service"
2. Keep the default Service Name: "MongoDB"
3. Select "Run service as Network Service user"
4. Click "Next"

![MongoDB Service Configuration](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/5.png)

### Step 6: Data Directory Configuration
1. Keep the default Data Directory path or change it if needed
2. Keep the default Log Directory path or change it if needed
3. Click "Next"

![MongoDB Data Directory Configuration](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/6.png)

### Step 7: Install MongoDB Compass (Optional)
1. Check "Install MongoDB Compass" if you want to install it during MongoDB installation
2. Click "Next"

![MongoDB Compass Installation Option](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/7.png)

### Step 8: Ready to Install
1. Review your installation settings
2. Click "Install" to begin the installation

![MongoDB Ready to Install](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/8.png)

### Step 9: Installation Progress
1. Wait for the installation to complete

![MongoDB Installation Progress](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/9.png)

### Step 10: Complete the Installation
1. Click "Finish" to exit the installer

![MongoDB Installation Complete](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/10.png)

## MongoDB Compass Installation

If you didn't install MongoDB Compass during the MongoDB installation, follow these steps:

### Step 1: Download MongoDB Compass
1. Visit the MongoDB Compass download page: [https://www.mongodb.com/try/download/compass](https://www.mongodb.com/try/download/compass)
2. Select the appropriate version for your Windows system (typically 64-bit)
3. Click "Download"

![MongoDB Compass Download Page](https://hevodata.com/learn/wp-content/uploads/2022/01/MongoDB-Compass-Windows-Installation-Step-1.png)

### Step 2: Extract the Downloaded File
1. After downloading, navigate to the location where the file was saved
2. Extract the file by right-clicking and selecting "Extract All" or using your preferred extraction tool

![MongoDB Compass Extract File](https://hevodata.com/learn/wp-content/uploads/2022/01/MongoDB-Compass-Windows-Installation-Step-2.png)

### Step 3: Run the MongoDB Compass Installer
1. Locate the extracted .exe file and double-click to run it
2. The installation will start automatically

![MongoDB Compass Installation Starting](https://hevodata.com/learn/wp-content/uploads/2022/01/MongoDB-Compass-Windows-Installation-Step-3.png)

### Step 4: Launch MongoDB Compass
1. After installation, MongoDB Compass will launch automatically
2. You'll see the connection screen

![MongoDB Compass Launch Screen](https://hevodata.com/learn/wp-content/uploads/2022/01/MongoDB-Compass-Windows-Installation-Step-4.png)

### Step 5: Configure Connection Settings
1. Select "Fill in connection fields individually" to manually configure your connection

![MongoDB Compass Connection Settings](https://hevodata.com/learn/wp-content/uploads/2022/01/MongoDB-Compass-Windows-Installation-Step-5.png)

### Step 6: Complete Setup
1. After configuring your connection settings, you're ready to use MongoDB Compass

![MongoDB Compass Ready](https://hevodata.com/learn/wp-content/uploads/2022/01/MongoDB-Compass-Windows-Installation-Step-6.png)

## Connecting MongoDB Compass to MongoDB

### Step 1: Launch MongoDB Compass
1. Open MongoDB Compass from your desktop or Start menu
2. You'll see the connection screen

![MongoDB Compass Connection Screen](https://hevodata.com/learn/wp-content/uploads/2022/01/MongoDB-Compass-Windows-Installation-Step-4.png)

### Step 2: Connect to MongoDB
1. For a local MongoDB installation, use the default connection string: `mongodb://localhost:27017`
2. Click "Connect"

![MongoDB Compass Connection](https://hevodata.com/learn/wp-content/uploads/2022/01/MongoDB-Compass-Windows-Installation-Step-5.png)

### Step 3: Explore MongoDB
1. Once connected, you'll see the list of databases
2. You can now create, view, and manage your MongoDB databases and collections

![MongoDB Compass Interface](https://hevodata.com/learn/wp-content/uploads/2022/01/MongoDB-Compass-Windows-Installation-Step-6.png)

## Verification

### Verify MongoDB Installation
1. Open Command Prompt
2. Type `mongod --version` and press Enter
3. You should see the MongoDB version information

![MongoDB Version Verification](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/11.png)

### Verify MongoDB Service
1. Open Command Prompt
2. Type `services.msc` and press Enter
3. Look for "MongoDB" in the services list
4. Ensure its status is "Running"

![MongoDB Service Verification](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/12.png)

## Running MongoDB Server and Shell

### Step 1: Start MongoDB Server
1. Open Command Prompt
2. Type `mongod` and press Enter
3. If you see an error about "C:/data/db/ not found", you need to create these directories

![MongoDB Server Start](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/13.png)

### Step 2: Create Required Folders (if needed)
1. Open C: drive and create a folder named "data"
2. Inside the "data" folder, create another folder named "db"

![Create MongoDB Data Folders](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/14.png)

### Step 3: Start MongoDB Shell
1. Open a new Command Prompt window (keep the mongod window open)
2. Type `mongosh` and press Enter
3. You are now connected to the MongoDB shell

![MongoDB Shell Start](https://www.geeksforgeeks.org/wp-content/uploads/20230613173318/15.png)

## Troubleshooting

### Common Issues and Solutions

1. **MongoDB service fails to start**
   - Check if the data directory exists and has proper permissions
   - Verify that port 27017 is not being used by another application

2. **Cannot connect to MongoDB from Compass**
   - Ensure MongoDB service is running
   - Check if the connection string is correct
   - Verify firewall settings are not blocking the connection

3. **MongoDB Compass crashes on startup**
   - Ensure your system meets the minimum requirements
   - Try reinstalling MongoDB Compass

## Additional Resources

- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [MongoDB Compass Documentation](https://www.mongodb.com/docs/compass/)
- [MongoDB Community Forums](https://www.mongodb.com/community/forums/)

---

This installation guide provides all the necessary steps to successfully install and configure MongoDB and MongoDB Compass on your Windows system. If you encounter any issues during installation, refer to the troubleshooting section or consult the official MongoDB documentation.

