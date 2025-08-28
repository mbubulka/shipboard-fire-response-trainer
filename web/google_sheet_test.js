// Simple HTML form to test the feedback submission
function doGet() {
  const html = `
    <!DOCTYPE html>
    <html>
      <head>
        <title>Test Feedback Form</title>
      </head>
      <body>
        <h2>Test Feedback Submission</h2>
        <div id="result"></div>
        <script>
          // Test data
          const testData = {
            session_id: 'test_' + Date.now(),
            scenario_id: 'test_scenario',
            difficulty_rating: 4,
            ai_helpfulness: 5,
            scenario_realism: 4,
            confidence_level: 3,
            training_level: 'novice',
            what_worked_well: 'Test feedback - things that worked',
            what_was_confusing: 'Test feedback - confusing items',
            suggested_improvements: 'Test feedback - suggestions',
            additional_comments: 'Test feedback - comments'
          };

          // Send test data
          fetch('${ScriptApp.getService().getUrl()}', {
            method: 'POST',
            body: JSON.stringify(testData)
          })
          .then(response => response.json())
          .then(data => {
            document.getElementById('result').innerHTML = 
              '<p style="color: green">✅ Test successful! Check your spreadsheet for the test entry.</p>' +
              '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
          })
          .catch(error => {
            document.getElementById('result').innerHTML = 
              '<p style="color: red">❌ Test failed: ' + error + '</p>';
          });
        </script>
      </body>
    </html>
  `;
  return HtmlService.createHtmlOutput(html);
}
