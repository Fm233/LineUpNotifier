package main

import (
	"log"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

type Entry struct {
	gorm.Model
	Count int
	ImgID int
}

type Store struct {
	gorm.Model
	Count int
}

func main() {
	// Connect to database
	dsn := "root:secret@tcp(mysql:3306)/data?charset=utf8mb4&parseTime=True&loc=Local"
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Panicln(err)
	}

	// Migrate database
	db.AutoMigrate(&Entry{})
	db.AutoMigrate(&Store{})

	// Define routes
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})
	r.POST("/entry", func(c *gin.Context) {
		// Parse input
		count, err := strconv.Atoi(c.PostForm("count"))
		if err != nil {
			c.JSON(405, gin.H{
				"success": false,
				"error":   err.Error(),
			})
		}
		imgID, err := strconv.Atoi(c.PostForm("img_id"))
		if err != nil {
			c.JSON(405, gin.H{
				"success": false,
				"error":   err.Error(),
			})
		}

		// Create element
		db.Create(&Entry{Count: count, ImgID: imgID})
		db.Create(&Store{Count: count})

		// Trim entries
		db.Where("created_at < ?", time.Now().Add(-time.Second*20)).Delete(&Entry{})

		// Send result
		c.JSON(201, gin.H{
			"success": true,
		})
	})
	r.GET("/avg", func(c *gin.Context) {
		// Get entries
		var entries []Entry
		result := db.Find(&entries)
		if result.Error != nil {
			c.JSON(404, gin.H{
				"success": false,
				"error":   result.Error.Error(),
			})
		}

		// Calculate weight base
		base := 0.0
		for i := 0; i < len(entries); i++ {
			base += float64(i + 1)
		}

		// Calculate data with biased weights
		count := len(entries)
		imgID := entries[count-1].ImgID
		s := 0.0
		for i, entry := range entries {
			s += float64(entry.Count*(i+1)) / base
		}
		tlb := entries[0].CreatedAt
		tub := entries[count-1].CreatedAt

		// Send result
		c.JSON(200, gin.H{
			"success": true,
			"tlb":     tlb.Format("2006-01-02 15:04:05"),
			"tub":     tub.Format("2006-01-02 15:04:05"),
			"s":       s,
			"count":   count,
			"img_id":  imgID,
		})
	})
	r.Run("0.0.0.0:8000") // listen and serve on 0.0.0.0:8000
}
