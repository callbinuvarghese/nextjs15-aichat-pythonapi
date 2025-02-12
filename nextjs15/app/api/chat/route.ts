// app/api/chat/route.jsx
import { NextResponse } from 'next/server';

export async function POST(req) {
  try {
    const { messages } = await req.json();
    const isHtml = false;
    console.log("Messages:", messages); // Log the URL
    console.log("isHtml:", isHtml); 

    const pythonApiUrl = isHtml ? 'http://127.0.0.1:5000/chat/html' : 'http://127.0.0.1:5000/chat/stream'; // Conditional URL
    const contentType = isHtml ? 'text/html' : 'text/event-stream'; // Conditional Content-Type
    
    console.log("Fetching from:", pythonApiUrl); // Log the URL

    const response = await fetch(pythonApiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ messages }),
    });

    if (!response.ok) {
      const errorData = await response.json(); // Try to get error details from Python
      return new NextResponse(JSON.stringify({ error: errorData || "Python API Error" }), {
        status: response.status,
        headers: {
          'Content-Type': 'application/json',
        },
      });
    }

    // Log the headers from the Python response
    console.log("Python API Response Headers:", response.headers);
    console.log("Python API Response Body:", response.body);
    const contentTypeHdr = response.headers.get('Content-Type')
    console.log("Python API Response Headers contentType:", contentTypeHdr);
    const mediaType = contentTypeHdr?.split(';')[0];
    console.log("Python API Response Headers contentType-mediaType:", mediaType);

    // Important: Return the response from the Python API directly
    return new NextResponse(response.body, { // Stream the body directly
      headers: {
        ...response.headers, // Copy headers from Python response
        'Content-Type': mediaType // Ensure correct Content-Type if needed
      }
    });


  } catch (error) {
    console.error("Error in POST request:", error);
    return new NextResponse(JSON.stringify({ error: "An error occurred" }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }
}

export const dynamic = 'force-dynamic';