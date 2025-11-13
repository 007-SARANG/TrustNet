@echo off
REM TrustNet 2.0 - Simple Post Analysis Test
REM This script sends test posts and you can see them analyzed in the terminal

echo ================================================================================
echo TrustNet 2.0 - Post Analysis Test
echo ================================================================================
echo.
echo Make sure:
echo 1. Backend server is running: python quick_start.py
echo 2. Check the terminal to see each post being analyzed!
echo.
pause

echo.
echo ================================================================================
echo Test 1: SUSPICIOUS POST (Fake News Keywords)
echo ================================================================================
curl -X POST http://localhost:8000/api/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"BREAKING: Scientists discover miracle cure that doctors don't want you to know about!\", \"source\": \"twitter\"}"
echo.
timeout /t 2 >nul

echo.
echo ================================================================================
echo Test 2: LEGITIMATE POST (Real News)
echo ================================================================================
curl -X POST http://localhost:8000/api/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"New study from Harvard Medical School shows promising results for cancer treatment.\", \"source\": \"academic\"}"
echo.
timeout /t 2 >nul

echo.
echo ================================================================================
echo Test 3: CLICKBAIT POST (Suspicious)
echo ================================================================================
curl -X POST http://localhost:8000/api/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"OMG! Celebrities reveal shocking secret to weight loss! Click here now!!!\", \"source\": \"facebook\"}"
echo.
timeout /t 2 >nul

echo.
echo ================================================================================
echo Test 4: NORMAL POST (Real)
echo ================================================================================
curl -X POST http://localhost:8000/api/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"The weather forecast for tomorrow shows a chance of rain in the afternoon.\", \"source\": \"twitter\"}"
echo.
timeout /t 2 >nul

echo.
echo ================================================================================
echo Test 5: CONSPIRACY POST (Fake)
echo ================================================================================
curl -X POST http://localhost:8000/api/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"Bill Gates wants to microchip everyone with 5G vaccines! Share before they delete this!\", \"source\": \"facebook\"}"
echo.

echo.
echo ================================================================================
echo ALL TESTS COMPLETE!
echo ================================================================================
echo.
echo Check the server terminal to see all the analyzed posts!
echo Also check your dashboard at: http://localhost:3000
echo.
pause
