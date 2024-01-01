# SalahCal
This Python script generates an iCalendar (.ics) file containing Islamic prayer times for the specified prayers for each day of the year. The timings are based on your local location and ISNA. The generated calendar is named "Salah".

## Prerequisites

- Python
- JSON file containing the prayer times data

## Usage

1. **Modify the Script:**
   Open the Python script and replace `/path/to/your/prayer_times.ics` with the desired path where you want to save the `.ics` file.

2. **Run the Script:**
   ```sh
   python main.py
3. **Import to Calendar App:**
  Import the generated .ics file to your preferred calendar application, creating a new calendar named "Salah".

4. **(Optional) Cancellation File:**
  If needed, you can uncomment the last few lines of the script to generate a cancellation .ics file. This can be imported to remove the events if required, but note that this feature may not be supported by all calendar applications.
