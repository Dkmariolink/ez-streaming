# Quick Start Tutorial

Welcome to EZ Streaming! This tutorial will get you up and running in just 5 minutes.

## What You'll Learn
- How to create your first profile
- How to add streaming applications
- How to configure launch delays
- How to launch all your apps at once

## Prerequisites
- EZ Streaming installed and running
- At least one streaming application installed on your computer (like OBS, Discord, or Spotify)

## Step 1: Understanding the Interface

When you first open EZ Streaming, you'll see:

### Main Components
- **Profile Dropdown:** Select or manage different streaming setups
- **Program List:** Shows applications in your current profile
- **Launch All Button:** Starts all applications in sequence
- **Action Buttons:** Individual launch/close controls for each app

### Default Setup
- EZ Streaming creates a "Default" profile automatically
- Two empty program rows are ready for your first applications

## Step 2: Adding Your First Application

Let's add OBS Studio as an example:

### Method 1: Using "Locate App by Name" (Recommended)
1. Click the **"Locate App by Name"** button in the first row
2. Type "OBS" in the search box
3. Click **"Search"**
4. EZ Streaming will find OBS and automatically fill in:
   - **Name:** "OBS Studio"
   - **Path:** The correct executable path

### Method 2: Browse Manually
1. Click the **"Browse"** button in the first row
2. Navigate to your application (e.g., `C:\Program Files\obs-studio\bin\64bit\obs64.exe`)
3. Select the executable file
4. The name will be auto-populated, or you can customize it

### Supported Applications
EZ Streaming has smart detection for 24+ streaming apps including:
- **Streaming Software:** OBS, Streamlabs, XSplit, Twitch Studio
- **Communication:** Discord, TeamSpeak
- **Music:** Spotify, VLC
- **Stream Tools:** Mix It Up, Touch Portal, VTube Studio

## Step 3: Adding More Applications

Let's add Discord as a second application:

1. Use the second program row
2. Click **"Locate App by Name"**
3. Search for "Discord"
4. Select the result

**Pro Tip:** EZ Streaming can find applications even if they're installed in non-standard locations!

## Step 4: Configuring Launch Order

Applications launch in the order they appear in the list:

### Reordering Applications
1. Click and drag the **drag handle** (≡) on the left of each row
2. Drop the application in your desired position
3. **Best Practice:** Put heavier applications (like OBS) first, lighter ones (like Spotify) last

### Why Order Matters
- Heavy applications need more time to load
- Some applications depend on others being ready first
- Good order reduces system strain during startup

## Step 5: Setting Up Launch Delays

Launch delays prevent overwhelming your system:

### Profile Default Delay
1. Look for the **"Default Launch Delay"** setting at the top
2. Set it to **5 seconds** (good starting point)
3. This delay applies between each application launch

### Per-Application Custom Delays
1. For heavy applications like OBS:
   - Check the **"Custom delay"** checkbox
   - Set a longer delay (e.g., **8 seconds**)
2. For lighter applications:
   - Leave unchecked to use the default delay

### Delay Best Practices
- **OBS/Streamlabs:** 8-10 seconds
- **Games:** 5-8 seconds  
- **Discord/Spotify:** 2-3 seconds
- **Browser tabs:** 1-2 seconds

## Step 6: Your First Launch

Now let's test everything:

1. Click the **"Launch All"** button
2. Watch the status updates in the bottom status bar
3. EZ Streaming will show:
   - "Launching [App Name]..."
   - "Waiting X seconds..."
   - Progress for each application

### What to Expect
- Applications will open in the order you set
- Delays will be respected between launches
- The UI remains responsive throughout
- Launch buttons change to "Launched" when apps are running

## Step 7: Managing Running Applications

Once applications are launched:

### Individual Control
- **Launch Button** becomes "Launched" and is disabled
- **Close Button** remains active to close individual apps
- Status indicators show which apps are running

### Closing Applications
- **Close Individual:** Click the "Close" button for specific apps
- **Close All:** Use the "Close All" button to shut down everything

## Step 8: Saving Your Work

EZ Streaming automatically saves:
- Your profile configuration
- Application paths and settings
- Launch delay preferences
- Window position and size

### Manual Save
- Changes are saved when you switch profiles
- Or when you close the application
- Green checkmark indicates saved status

## Creating Additional Profiles

For different streaming scenarios:

### Example Profiles
- **Gaming Stream:** OBS + Discord + Spotify + Game
- **Art Stream:** OBS + Art Software + Reference Browser + Music
- **Podcast:** Recording Software + Skype + Notes App + Music

### Creating a New Profile
1. Click the **dropdown arrow** next to the profile name
2. Select **"New Profile"**
3. Name it (e.g., "Gaming Setup")
4. Add applications specific to that scenario

## Advanced Quick Tips

### Performance Optimization
- **System with 8GB+ RAM:** Default 5-second delays are fine
- **System with 4GB RAM:** Use longer delays (7-10 seconds)
- **SSD Storage:** Can use shorter delays
- **HDD Storage:** Use longer delays

### Troubleshooting Common Issues
- **App won't launch:** Check the path is correct
- **System slows down:** Increase launch delays
- **App launches but crashes:** Try launching it manually first
- **Path not found:** Use "Browse" to manually locate the executable

### Power User Features
- **Drag and Drop:** Reorder applications easily
- **Profile Duplication:** Copy existing profiles as templates
- **Steam Games:** EZ Streaming can find Steam games automatically
- **Process Monitoring:** See which apps are actually running

## Next Steps

Now that you have the basics:

1. **Experiment with different profiles** for various streaming scenarios
2. **Fine-tune your launch delays** based on your system performance
3. **Explore advanced features** like process management
4. **Read about [Profile Management](Profile-Management.md)** for power user features

## Common First-Time Questions

**Q: How many applications can I add?**  
A: No hard limit! Most users have 3-8 applications per profile.

**Q: Can I add non-streaming applications?**  
A: Absolutely! Add any Windows executable you regularly use.

**Q: What if EZ Streaming can't find my application?**  
A: Use the "Browse" button to manually locate the executable file.

**Q: Can I change the order after adding applications?**  
A: Yes! Just drag and drop using the handles on the left.

**Q: Do I need to save manually?**  
A: No, EZ Streaming auto-saves your changes.

## Congratulations! 🎉

You've successfully set up your first EZ Streaming profile! You can now:
- Launch multiple applications with one click
- Switch between different streaming setups
- Save time on your pre-stream routine

**Ready for more?** Check out [Profile Management](Profile-Management.md) to learn about advanced profile features!
