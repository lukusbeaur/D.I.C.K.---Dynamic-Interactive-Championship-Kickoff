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

// TODO: create timer and total data pulled variables and implement them into code
func main() {
	file, err := os.Open("C:/Users/lukus/Documents/DICK/Masterlink.csv")
	if err != nil {
		log.Fatalf("Unable to locate or open file: %s\n", err)
	}
	defer file.Close()
	//reader for getting csvs form master link
	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		log.Fatalf("Unable to read file: %s", err)
	}
	//for each url do the thing
	//TODO create an if statement that if there is a URL inside the left off file than search
	//cont: for index of that url in the master link file and start loop from there.
	for _, record := range records {
		url := record[0]
		fmt.Println("Processing URL:", url)

		scrapeURL(url)
	}

}
func scrapeURL(url string) {
	//fmt.Println(url)
	//TODO: add regex to find the dates too
	//TODO add regex into function
	//find team name and data type inside URL
	re := regexp.MustCompile(`/([a-z_]+)/([^/]+)-Match-Logs-`)
	match := re.FindStringSubmatch(url)
	var teamName, dataType string
	//TODO: create the writer functions to be dynamic, inside a function
	//init the csv file writer------------------------------------------>
	dir := "C:/Users/lukus/Documents/DICK/TeamData"
	fName := fmt.Sprintf("%s/%s-%s.csv", dir, teamName, dataType)
	//create writer for Team Data,

	createFile(fName)
	/*file, err := os.Create(fName)
	if err != nil {
		log.Fatalf("Unable to create file %q: %s\n", fName, err)
	}
	*/
	writer := csv.NewWriter(file)
	defer writer.Flush()
	//create writer for failed team data------------------------------->
	createFile(fName)
	failfName := fmt.Sprintf("%s/url_Failure.csv", dir)
	/*failfile, err := os.Create(failfName)
	if err != nil {
		log.Fatalf("Unable to create file %q: %s\n", fName, err)
	}
	*/
	failwriter := csv.NewWriter(failfile)
	defer failwriter.Flush()
	//TODO: create function to handle the failedwriter issue
	//TODO: create function to capture last URL used, put in file.
	//if regex fails to pull team name or data type from url------------->
	if len(match) > 2 {
		teamName = match[2]
		dataType = match[1]
	} else {
		teamName = "Teamname"
		dataType = "Datatype"
		if err := failwriter.Write([]string{url}); err != nil {
			log.Fatalf("Unable to write to file : %s\n", err)
		}
	}
	fmt.Println("Extracted data type:", dataType)
	fmt.Println("Extracted team name:", teamName)

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
			//dataRow := row.Attr("data-row")
			//classRow := row.Attr("class")
			parentTag := row.DOM.Parent().Nodes[0].Data
			//fmt.Printf("currently on Class: %s\nrowData: %s\n", classRow, dataRow)

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
				//ok this should create the header. lets try
				//fmt.Println(rowIndex)
				//for now I removed the if statement ot see wtf is going on
				rowData = append(rowData, cell.Text)

			})

			err := writer.Write(rowData)
			if err != nil {
				log.Fatalf("Unable to write data to file: %s\n", err)
			}
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
func createFile(filepath string) *os.File {
	file, err := os.Create(filepath)
	if err != nil {
		log.Fatalf("Unable to create file %q: %s\n", filepath, err)
	}
	return file
}
func write
