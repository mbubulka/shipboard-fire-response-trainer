// Feedback collection function
const { MongoClient } = require('mongodb');

// Get these from Netlify environment variables
const MONGODB_URI = process.env.MONGODB_URI;
const DB_NAME = 'feedback_db';

let cachedDb = null;

async function connectToDatabase() {
  if (cachedDb) {
    return cachedDb;
  }
  
  const client = await MongoClient.connect(MONGODB_URI);
  const db = client.db(DB_NAME);
  cachedDb = db;
  return db;
}

exports.handler = async (event, context) => {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    // Parse the incoming request
    const data = JSON.parse(event.body);
    
    // Validate required fields
    const requiredFields = [
      'session_id', 
      'scenario_id', 
      'difficulty_rating',
      'ai_helpfulness', 
      'scenario_realism', 
      'confidence_level',
      'training_level'
    ];

    for (const field of requiredFields) {
      if (!data[field]) {
        return {
          statusCode: 400,
          body: JSON.stringify({ 
            success: false,
            error: `Missing required field: ${field}`
          })
        };
      }
    }

    // Add timestamp
    data.timestamp = new Date().toISOString();

    // Connect to database
    const db = await connectToDatabase();
    const collection = db.collection('feedback');

    // Store the feedback
    await collection.insertOne(data);

    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        message: 'Feedback stored successfully'
      })
    };

  } catch (error) {
    console.error('Error storing feedback:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: 'Error storing feedback'
      })
    };
  }
};
