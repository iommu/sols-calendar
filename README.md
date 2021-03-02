# sols-ics
A utility to create an ical (.ics) file from the UOW sols calendar

# running
* Requires Python 3

Download the python ics library
`pip install ics`

Go to the sols calendar and download the webpage with `CMD/CTRL + s` into this directory. This should be saved to a file "My SOLS - My Timetable.html"

Run the convert.py file with the input argument of the downloaded file

`$ python ./convert.py ./My\ SOLS\ -\ My\ Timetable.html`

specifiying the first monday of the semester and the week on which the break is when prompted.

Import the .ics file into the calendar application of your choice (as a seperate calendar for easy deletion incase of mess up) 