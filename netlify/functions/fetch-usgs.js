// Netlify Function to fetch USGS water data
// This function proxies USGS API calls to avoid CORS issues

exports.handler = async (event, context) => {
  // Enable CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
    'Content-Type': 'application/json',
    'Cache-Control': 'public, max-age=900' // 15 minutes
  };

  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: 'ok'
    };
  }

  try {
    const { siteNumber = '01646500', days = 7 } = event.queryStringParameters || {};

    // Validate input
    if (!siteNumber || siteNumber.length < 8) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid site number' })
      };
    }

    const endDate = new Date();
    const startDate = new Date(endDate.getTime() - days * 24 * 60 * 60 * 1000);

    const startStr = startDate.toISOString().split('T')[0];
    const endStr = endDate.toISOString().split('T')[0];

    // Fetch from USGS
    const usgsUrl = `https://waterservices.usgs.gov/nwis/iv/?sites=${siteNumber}&parameterCd=00060&startDT=${startStr}&endDT=${endStr}&format=json`;

    const response = await fetch(usgsUrl, {
      timeout: 10000
    });

    if (!response.ok) {
      throw new Error(`USGS API returned status ${response.status}`);
    }

    const data = await response.json();

    // Extract and format data
    if (!data.value || !data.value.timeSeries || data.value.timeSeries.length === 0) {
      throw new Error('No data returned from USGS');
    }

    const timeSeries = data.value.timeSeries[0];
    const values = timeSeries.values[0].value;

    const formattedData = values
      .map(v => ({
        time: v.dateTime,
        flow: parseFloat(v.value),
        raw: v.value
      }))
      .filter(v => !isNaN(v.flow) && v.flow > 0)
      .sort((a, b) => new Date(a.time) - new Date(b.time));

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        siteNumber,
        stationName: timeSeries.sourceInfo.siteName,
        data: formattedData,
        count: formattedData.length,
        startDate: startStr,
        endDate: endStr,
        lastUpdated: new Date().toISOString()
      })
    };
  } catch (error) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      })
    };
  }
};
