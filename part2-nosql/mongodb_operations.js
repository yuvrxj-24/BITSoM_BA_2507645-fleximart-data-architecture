// =========================================================
// FlexiMart - MongoDB Operations (Task 2.2)
// File: mongodb_operations.js
// Run: mongosh "C:\Users\navya\Desktop\ASG2\mongodb_operations.js"
// =========================================================

db = db.getSiblingDB("fleximart_nosql");

// ------------------------------
// Operation 1: Load Data (1 mark)
// ------------------------------
const fs = require("fs");
const data = JSON.parse(
  fs.readFileSync("C:\\Users\\navya\\Desktop\\ASG2\\products_catalog.json", "utf-8")
);

db.products.drop();
db.products.insertMany(data);

print("\n=== Operation 1: Load Data ===");
print("Documents in products:", db.products.countDocuments());

// ------------------------------
// Operation 2: Basic Query (2 marks)
// ------------------------------
print("\n=== Operation 2: Electronics price < 50000 (name, price, stock) ===");
printjson(
  db.products
    .find(
      { category: "Electronics", price: { $lt: 50000 } },
      { _id: 0, name: 1, price: 1, stock: 1 }
    )
    .toArray()
);

// ------------------------------
// Operation 3: Review Analysis (2 marks)
// ------------------------------
print("\n=== Operation 3: Products with avg rating >= 4.0 ===");
printjson(
  db.products.aggregate([
    { $match: { reviews: { $exists: true, $ne: [] } } },
    { $addFields: { avg_rating: { $avg: "$reviews.rating" } } },
    { $match: { avg_rating: { $gte: 4.0 } } },
    { $project: { _id: 0, product_id: 1, name: 1, category: 1, avg_rating: 1 } },
    { $sort: { avg_rating: -1 } }
  ]).toArray()
);

// ------------------------------
// Operation 4: Update Operation (2 marks)
// ------------------------------
print("\n=== Operation 4: Add review to ELEC001 ===");
const updateResult = db.products.updateOne(
  { product_id: "ELEC001" },
  {
    $push: {
      reviews: {
        user_id: "U999",
        username: "NewUser",
        rating: 4,
        comment: "Good value",
        date: new Date()
      }
    }
  }
);
printjson(updateResult);

print("\nVerify ELEC001 last review:");
printjson(
  db.products.find(
    { product_id: "ELEC001" },
    { _id: 0, product_id: 1, name: 1, reviews: { $slice: -1 } }
  ).toArray()
);

// ------------------------------
// Operation 5: Complex Aggregation (3 marks)
// ------------------------------
print("\n=== Operation 5: Avg price by category ===");
printjson(
  db.products.aggregate([
    {
      $group: {
        _id: "$category",
        avg_price: { $avg: "$price" },
        product_count: { $sum: 1 }
      }
    },
    { $project: { _id: 0, category: "$_id", avg_price: 1, product_count: 1 } },
    { $sort: { avg_price: -1 } }
  ]).toArray()
);
