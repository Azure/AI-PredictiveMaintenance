# Create Cluster Using AZTK and spin up Jupyter Notebooks

## Create Spark Cluster:

    Go to the Function App console and run the below command 
        D:\home\python364x64\python.exe %Aztk_Spark_Path% “clusterusername” “clusterpassword”

## Access Jupyter Notebooks available in the cluster 

1.	**Using SSH Client**

    Run the below command

        ssh username@cluster-IpAddress -p MasterNodePortNumber -L 8888:127.0.0.1:8888
        Example : ssh admin@52.178.100.71 -p 50000 -L 8888:127.0.0.1:8888

2.	**Using Putty**

    Step 1:
        ![Putty](/img/Putty_1.png)

        Host Name: Spark Cluster IP created through AZTK
        Port: Master Port Number

    Step 2:
        ![Putty](/img/Putty_2.png)
        
        Source port: Port you want the notebooks to be forwarded to in your local machine
        Destination: localhost:8888 (always)
        Then click on Add and open the SSH connection 

    Step 3: Open localhost:8888 in your local machine
        ![Putty](/img/Putty_3.png)

3.	**Using AZTK**

        **Install Aztk in your local machine**

            1.	Clone the repo
 		    git clone -b stable https://www.github.com/azure/aztk
            You can also clone directly from master to get the latest bits
            git clone https://www.github.com/azure/aztk

        2.	Use pip to install required packages (requires python 3.5+ and pip 9.0.1+)
                pip install -r requirements.txt

        3.	Use setup tools:
            pip install -e .

        4.	Initialize the project in a directory [This will automatically create a .aztk folder with config files in your working directory]:
            aztk spark init
                                      
        **Fill in the following fields in your .aztk/secrets.yaml file**

            shared_key:
    	        batch_account_name:
                batch_account_key: 
                batch_service_url: 
     	        storage_account_name: 
                storage_account_key: 
                storage_account_suffix: 

        All the above field values are available as environment variables in the function app service which can be accessed at the function App Console