// Google Apps Script code to handle feedback submissions
function doPost(e) {
  // Get the spreadsheet and sheet
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('Feedback') || ss.insertSheet('Feedback');
  
  try {
    // Parse the incoming data
    const data = JSON.parse(e.postData.contents);
    
    // If this is the first entry, add headers
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        'Timestamp',
        'Session ID',
        'Scenario ID',
        'Difficulty Rating',
        'AI Helpfulness',
        'Scenario Realism',
        'Confidence Level',
        'Training Level',
        'What Worked Well',
        'What Was Confusing',
        'Suggested Improvements',
        'Additional Comments'
      ]);
    }
    
    // Add the new row of data
    sheet.appendRow([
      new Date(),
      data.session_id,
      data.scenario_id,
      data.difficulty_rating,
      data.ai_helpfulness,
      data.scenario_realism,
      data.confidence_level,
      data.training_level,
      data.what_worked_well || '',
      data.what_was_confusing || '',
      data.suggested_improvements || '',
      data.additional_comments || ''
    ]);
    
    // Return success response
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      message: 'Feedback recorded successfully'
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    // Return error response
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// Test function to verify the script is working
function testScript() {
  Logger.log('Script is ready to receive feedback!');
}
