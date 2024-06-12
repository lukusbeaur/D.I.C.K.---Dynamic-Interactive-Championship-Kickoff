package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"regexp"
	"time"

	"github.com/gocolly/colly"
	//"github.com/gocolly/colly/debug"
)

// TODO: create timer and total data pulled variables and implement them into code----->
func main() {
	starttime := time.Now()
	elapsedTime := time.Since((starttime))
	//Open tracker CSV file for URL. This will track where you are in the main list
	//and if there is an interuption the loop will start on the last saved URL -------->

	//Open Main CSV file for urls. Handle errors encapsulated in openfileandReadAll
	//Create a reader for the main CSV file, Save all records for iteration------------>
	file, reader := openFileReadAll("C:/Users/lukus/Documents/DICK/Masterlink.csv")
	defer file.Close()
	records, err := reader.ReadAll()
	if err != nil {
		log.Fatalf("Unable to read file: %s", err)
	}
	//TODO create an if statement that if there is a URL inside the left off file than
	//cont: searchfor index of that url in the master link file and start loop from there.
	//Iterate through the records readall object. for each URL in the object scrape the
	//table and save it to the 'Datatype_teamname.csv ---------------------------------->
	fmt.Printf("The time is %s. Starting to pull data\n", starttime)
	for _, record := range records {
		url := record[0]
		//track current URL here
		writeCurrentURL(url, "C:/Users/lukus/Documents/DICK/last_URL.csv")
		fmt.Println("Processing URL:", url)
		scrapeURL(url)
	}
	//TODO: create a graceful shutdown function. Channels, SIGS, and <- make.
	fmt.Printf("Total Elapsed time: %s\n", elapsedTime)
}
func scrapeURL(url string) {
	var teamName, dataType, season string
	//TODO: add regex to find the dates too
	//TODO add regex into function
	//find team name and data type inside URL
	re := regexp.MustCompile(`/([a-z_]+)/([^/]+)-Match-Logs-`)
	dateRe := regexp.MustCompile(`\b(\d{4}(?:-\d{4})?)\b`)
	match := re.FindStringSubmatch(url)
	dmatch := dateRe.FindStringSubmatch(url)

	//DONE: create function to handle the failedwriter issue
	//DONE/ Checked/ Remove line on next commit: create function to capture last URL used, put in file.
	//if regex fails to pull team name or data type from url it is placed in an error
	//File. To keep track of potential erros. ------------------------------------------>
	if len(match) > 2 && len(dmatch) > 1 {
		teamName = match[2]
		dataType = match[1]
		season = dmatch[1]
	} else {
		teamName = "Teamname_error"
		dataType = "Datatype_error"
		season = "seasonDate_error"
		dir := "C:/Users/lukus/Documents/DICK/TeamData"
		appendToFile(fmt.Sprintf("%s/url_Failure.csv", dir), []string{url})
		fmt.Printf("Failed to extract data from URL: %s\n", url)
		return
	}
	fmt.Printf("The season folder being made is %s\n", season)
	fmt.Println("Extracted data type:", dataType)
	fmt.Println("Extracted team name:", teamName)
	fmt.Println("Extracted season Date:", season)

	//DONE, checked, remove line on next commit: create the writer functions to be dynamic, inside a function
	//TODO: create files in the local directory  insdie new folder. remove direct dir
	//cont: replacte with relative dir.
	//init the csv file writer and create files. Writer: for URL table data, fwriter to
	//cont: keep track of any errors on regex errors  ---------------------------------->
	dir := fmt.Sprintf("C:/Users/lukus/Documents/DICK/TeamData/%s/", season)
	err := os.MkdirAll(dir, os.ModePerm)
	if err != nil {
		log.Fatalf("unable to create directory %q: %s\n", dir, err)
	}
	_, writer := createFile(fmt.Sprintf("%s%s-%s.csv", dir, teamName, dataType))
	defer writer.Flush()

	//START: initiate a collector object
	c := colly.NewCollector(
		colly.AllowedDomains("fbref.com"),
		//colly.Async(true),
		//colly.Debugger(&debug.LogDebugger{}),
	)
	var startTime time.Time
	var requestSize int
	//lets try and connect first and print the call back of the request
	//Start timer
	c.OnRequest(func(r *colly.Request) {
		startTime = time.Now()
		fmt.Println("Visiting:", r.URL.String())
	})
	//on response lets check size of data
	c.OnResponse(func(r *colly.Response) {
		requestSize += len(r.Body)
	})
	c.OnScraped(func(r *colly.Response) {
		elapsedTime := time.Since((startTime))
		fmt.Printf("Elapsed Time for one URL: %s\n", elapsedTime)
		fmt.Printf("Total Data pulled: %d bytes\n", requestSize)
	})

	//random delay rate limiter
	c.Limit(&colly.LimitRule{
		DomainGlob:  "fbref.com",
		Parallelism: 1,
		RandomDelay: 3 * time.Second,
	})

	//search for table and pull data, putting into CSV------------------------------>
	c.OnHTML("#matchlogs_for", func(e *colly.HTMLElement) {
		//i need to keep track of the rows and columns for easy parcing.
		rowIndex := 0
		e.ForEach("tr", func(_ int, row *colly.HTMLElement) {
			var rowData []string
			parentTag := row.DOM.Parent().Nodes[0].Data

			if rowIndex == 0 {
				rowIndex++
				return
			}
			if row.Attr("class") == "spacer partial_table" {
				//fmt.Printf("Skipping row with class: %s\n", row.Attr("class"))
				return
			}
			if parentTag == "tfoot" {
				return
			}
			row.ForEach("th, td", func(_ int, cell *colly.HTMLElement) {
				rowData = append(rowData, cell.Text)

			})

			writeRecord(writer, rowData)
			rowIndex++
		})
	})
	c.Wait()
	//start and check for error
	err = c.Visit(url)
	if err != nil {
		fmt.Println("Error visiting the site:", err)
	}
}
func createFile(filepath string) (*os.File, *csv.Writer) {
	file, err := os.Create(filepath)
	if err != nil {
		log.Fatalf("Unable to create file %q: %s\n", filepath, err)
	}
	writer := csv.NewWriter(file)
	return file, writer
}
func writeRecord(writer *csv.Writer, record []string) {
	if err := writer.Write(record); err != nil {
		log.Fatalf("Unable to write record to file :%s\n", err)
	}
	writer.Flush()
}
func openFileReadAll(filepath string) (*os.File, *csv.Reader) {
	file, err := os.Open(filepath)
	if err != nil {
		log.Fatalf("Unable to open or locate file: %s\n", err)
	}
	reader := csv.NewReader(file)
	if err != nil {
		log.Fatalf("Unable to read file: %s", err)
	}
	return file, reader
}
func writeCurrentURL(record, filepath string) {
	//Create file, _ file object, returns writer object. this will overwrite ---------->
	file, writer := createFile(filepath)
	defer file.Close()
	defer writer.Flush()
	//write records to file' WriteRecord only works with arrays, so you musth convert-->
	records := []string{record}
	writeRecord(writer, records)
}
func appendFileAndWriter(filePath string) (*os.File, *csv.Writer) {
	//This will open file and append lines instead of overwriting it ------------------>
	file, err := os.OpenFile(filePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatalf("Unable to open file %q: %s\n", filePath, err)
	}
	writer := csv.NewWriter(file)
	return file, writer
}
func appendToFile(filepath string, record []string) {
	file, writer := appendFileAndWriter(filepath)
	defer file.Close()
	defer writer.Flush()

	writeRecord(writer, record)
}
