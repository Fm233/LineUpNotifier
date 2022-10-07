package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"net/url"
	"strconv"
)

func resp2result(resp *http.Response) map[string]interface{} {
	if resp.StatusCode != 201 && resp.StatusCode != 200 {
		log.Println(resp.StatusCode)
		log.Fatalln("Status code is not 200 or 201")
	}
	if resp.Body != nil {
		defer resp.Body.Close()
	}
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}
	var result map[string]interface{}
	err = json.Unmarshal(body, &result)
	if err != nil {
		log.Fatalln(err)
	}
	if result["success"] != true {
		log.Fatalln("Response.success isn't true")
	}
	return result
}

func main() {
	// Define temp variables and functions
	last_id := 0
	post := func(count int) {
		resp, err := http.PostForm("http://go-server:8000/entry", url.Values{
			"count":  {strconv.Itoa(count)},
			"img_id": {strconv.Itoa(last_id)},
		})
		if err != nil {
			log.Fatalln(err)
		}
		resp2result(resp)
		last_id++
	}
	get := func() {
		resp, err := http.Get("http://go-server:8000/avg")
		if err != nil {
			log.Fatalln(err)
		}
		result := resp2result(resp)
		log.Println(result)
	}

	// Call test functions
	for i := 5; i < 15; i++ {
		post(i)
	}
	get()
}
