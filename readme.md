# Before running the Video_Editor.py file, you need to setup you enviroment.

## Step 1
### To set up your enviroment you will need to install 3 python libraries before running the code.



* psycopg2-binary
* moviepy
* PyYAML

You can use the following code to install these modules:<br>
`pip install psycopg2 moviepy pyyaml`


## Step 2
### Create your PostgresSQL Database if you haven't already.

You will need to create a [PostgresSQL](https://www.postgresql.org/ "PostgresSQL Website").
If you don't have PostgresSQL in you computer, you can use the link above to download it.


## Step 3
### Create a Configuration file, with the Database and Video details.

Include the PostgresSQL Database details into a config file, in this case `config.yml`. You will need to update the details of your Database in this config file.

`postgresql:`<br>
  &nbsp;&nbsp;`dbname: mydatabase`<br>
  &nbsp;&nbsp;`user: myuser`<br>
  &nbsp;&nbsp;`password: mypassword`<br>
  &nbsp;&nbsp;`host: localhost`<br>
  &nbsp;&nbsp;`port: 5432`<br>

Also you will need to update the Video details, like the file name, the output folder, and the report folder.

`video_processing:`<br>
  &nbsp;&nbsp;`input_file: airshow.mp4`<br>
  &nbsp;&nbsp;`output_folder: output_clips`<br>
  &nbsp;&nbsp;`report_folder: report`<br>

- - -

### Now you can run Video_Editor.py file. Enjoy!
