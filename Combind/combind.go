package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	// Directory containing the CSV files
	var counter int
	csvDir := "../TeamData/2023"
	savedata := "../TeamData/combine"
	abspath, _ := filepath.Abs(savedata)
	fmt.Printf("Saving directory: %s\n", savedata)
	fmt.Printf("Absolute path of saving directory: %s\n", abspath)

	// Create the save directory if it doesn't exist
	err := os.MkdirAll(savedata, os.ModePerm)
	if err != nil {
		fmt.Println("Error creating save directory:", err)
		return
	}

	// Read all CSV files in the directory
	files, err := os.ReadDir(csvDir)
	if err != nil {
		fmt.Println("Error reading directory:", err)
		return
	}

	// Map to hold concatenated data by team name
	teamData := make(map[string][][]string)
	headers := make(map[string][]string)
	firstIteration := make(map[string]bool)

	for _, file := range files {
		if !file.IsDir() && filepath.Ext(file.Name()) == ".csv" {
			filePath := filepath.Join(csvDir, file.Name())

			// Extract the team name (all parts before the last hyphen)
			fileNameWithoutExt := strings.TrimSuffix(file.Name(), filepath.Ext(file.Name()))
			parts := strings.Split(fileNameWithoutExt, "-")
			teamName := strings.Join(parts[:len(parts)-1], "-")

			fmt.Printf("Processing File: %s\n Team Name: %s\n File Path: %s\n", file.Name(), teamName, filePath)

			// Open CSV file
			f, err := os.Open(filePath)
			if err != nil {
				fmt.Println("Error opening file:", filePath, err)
				continue
			}
			defer f.Close()

			// Read CSV data
			reader := csv.NewReader(f)
			records, err := reader.ReadAll()
			if err != nil {
				fmt.Println("Error reading CSV data:", filePath, err)
				continue
			}

			if len(records) > 0 {
				if !firstIteration[teamName] {
					// First iteration, include everything
					headers[teamName] = records[0]
					teamData[teamName] = records[1:]
					firstIteration[teamName] = true
					fmt.Printf("First file for team %s, including all columns.\n", teamName)
				} else {
					// Skip the first 9 columns in subsequent files
					headers[teamName] = append(headers[teamName], records[0][9:]...)

					for i, row := range records[1:] {
						if len(teamData[teamName]) <= i {
							teamData[teamName] = append(teamData[teamName], row[9:])
						} else {
							teamData[teamName][i] = append(teamData[teamName][i], row[9:]...)
						}
					}
					fmt.Printf("Processed additional file for team %s, skipping first 9 columns.\n", teamName)
				}
			}
		}
	}

	// Write concatenated data to new CSV files
	for team, data := range teamData {
		outputFileName := filepath.Join(savedata, team+".csv")
		outputFile, err := os.Create(outputFileName)
		if err != nil {
			fmt.Println("Error creating file:", outputFileName, err)
			continue
		}
		defer outputFile.Close()

		writer := csv.NewWriter(outputFile)

		// Write headers
		if err := writer.Write(headers[team]); err != nil {
			fmt.Println("Error writing headers to file:", outputFileName, err)
		}

		// Write data rows
		for _, record := range data {
			if err := writer.Write(record); err != nil {
				fmt.Println("Error writing record to file:", outputFileName, err)
			}
		}
		writer.Flush()

		if err := writer.Error(); err != nil {
			fmt.Println("Error flushing writer:", outputFileName, err)
		}
	}

	fmt.Println("CSV files combined successfully")
	fmt.Printf("Combine %d teams", counter)
}
