#!/bin/bash

echo "🐦 Flappy Bird Java Game - Deployment Script"
echo "============================================="

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "❌ Java is not installed. Please install Java JDK 8 or higher."
    exit 1
fi

if ! command -v javac &> /dev/null; then
    echo "❌ Java compiler (javac) is not installed. Please install Java JDK."
    exit 1
fi

echo "✅ Java found: $(java -version 2>&1 | head -1)"

# Compile the game
echo "🔨 Compiling Java files..."
javac *.java

if [ $? -eq 0 ]; then
    echo "✅ Compilation successful!"
else
    echo "❌ Compilation failed!"
    exit 1
fi

# Create JAR file
echo "📦 Creating JAR file..."
echo -e "Manifest-Version: 1.0\nMain-Class: App\n" > MANIFEST.MF
jar cfm FlappyBird.jar MANIFEST.MF *.class *.png

if [ $? -eq 0 ]; then
    echo "✅ JAR file created: FlappyBird.jar"
else
    echo "❌ JAR creation failed!"
fi

# Run the game
echo ""
echo "🚀 Starting Flappy Bird Game..."
echo "   Press SPACE to start/jump/restart"
echo "   Close the window to exit"
echo ""

# Try to run the game
if [ -n "$DISPLAY" ]; then
    echo "🖥️  Running with display: $DISPLAY"
    java App
else
    echo "⚠️  No DISPLAY variable set. Trying to run anyway..."
    java App
fi

echo ""
echo "🎮 Game session ended. Thanks for playing!"