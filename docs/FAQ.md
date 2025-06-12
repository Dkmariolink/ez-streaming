# Frequently Asked Questions (FAQ)

Common questions and answers about EZ Streaming to help you get the most out of the application.

## Getting Started

### What is EZ Streaming?
**EZ Streaming** is a free, open-source application launcher designed specifically for content creators and streamers. It allows you to launch multiple applications (like OBS, Discord, Spotify, games, etc.) with a single click, complete with configurable delays and process management.

### How much does EZ Streaming cost?
**EZ Streaming is completely free** and always will be. It's open-source software licensed under GPLv3, meaning you can use it, modify it, and redistribute it freely. There are no premium versions, subscriptions, or hidden costs.

### Do I need to install EZ Streaming?
**No installation required!** EZ Streaming is a portable application. Simply download the executable file, place it in a folder of your choice, and run it. All your settings are saved automatically.

### What operating systems does EZ Streaming support?
Currently, **EZ Streaming supports Windows 10 and 11 (64-bit)**. Cross-platform support for macOS and Linux is planned for future releases.

## Features and Functionality

### How many applications can I add to a profile?
**There's no hard limit** on the number of applications per profile. Most users typically have 3-8 applications per profile, but you can add as many as your system can handle. The interface is designed to scale with your needs.

### Can I use EZ Streaming with applications that aren't on the supported list?
**Absolutely!** While EZ Streaming has smart detection for 24+ popular streaming applications, it can launch **any Windows executable**. Use the "Browse" button to add any program you want to include in your profiles.

### What's the difference between "Launch" and "Launch All"?
- **Launch:** Starts a single application immediately
- **Launch All:** Starts all applications in the profile sequentially, respecting the configured launch delays

### How do launch delays work?
**Launch delays** prevent system overload by waiting between application launches. You can set:
- **Profile default delay:** Applied to all applications in the profile
- **Custom delays:** Per-application overrides for specific timing needs
- **No delay:** The first application in a profile launches immediately

### Can I reorder applications in a profile?
**Yes!** Click and drag the **handle (≡)** on the left side of any application row to reorder them. Applications launch in the order they appear in the list.

## Technical Questions

### Why does Windows show a security warning when I run EZ Streaming?
This is **completely normal** and happens because we haven't code-signed the executable yet. To run EZ Streaming:
1. Click **"More info"** in the Windows SmartScreen dialog
2. Click **"Run anyway"**

The software is completely safe - you can verify this by checking our open-source code on GitHub.

### Does EZ Streaming collect any data or phone home?
**No data collection whatsoever.** EZ Streaming:
- Doesn't collect usage statistics
- Doesn't send any data over the internet
- Works completely offline
- Stores all configuration locally on your computer

### Why is my antivirus flagging EZ Streaming?
Some antivirus programs show **false positives** for applications built with PyInstaller (our build tool). This is common and not a real threat. To resolve this:
1. Add EZ Streaming to your antivirus whitelist
2. Download from our official GitHub releases page to ensure you have the authentic version

### How much system resources does EZ Streaming use?
**EZ Streaming is very lightweight:**
- **Memory:** ~50-100 MB while running
- **CPU:** Minimal usage except during application launches
- **Storage:** ~15-20 MB for the executable, ~10 MB for configuration
- **Network:** None - works completely offline

## Profile Management

### What's the difference between profiles?
**Profiles** are different configurations of applications for various scenarios:
- **Gaming Profile:** OBS + Discord + Spotify + Game Launcher
- **Art Profile:** OBS + Art Software + Reference Browser + Music
- **Podcast Profile:** Recording Software + Communication Apps + Notes

Each profile has its own applications, launch order, and delay settings.

### Can I copy applications between profiles?
**Currently:** You need to manually add applications to each profile  
**Future Feature:** Profile import/export and "copy from another profile" features are planned for upcoming releases.

### Why can't I rename or delete the Default profile?
The **Default profile is protected** to ensure you always have at least one working profile. It cannot be renamed or deleted, but you can modify its applications and settings freely.

### How many profiles can I create?
**No limit** on the number of profiles, but for practical organization, most users have 5-8 profiles. The interface remains responsive even with many profiles.

## Application Management

### Why can't EZ Streaming find my application?
If the smart search can't find your application:
1. **Check spelling:** Try different variations of the application name
2. **Verify installation:** Ensure the application is actually installed
3. **Use Browse:** Manually locate the executable file
4. **Check common locations:** Some applications install to unusual directories

### My application launches but doesn't work properly. What's wrong?
**Common causes and solutions:**
- **Wrong executable:** Some applications have multiple .exe files - try different ones
- **Needs administrator rights:** Run EZ Streaming as administrator
- **Requires specific startup order:** Adjust the launch order in your profile
- **Insufficient launch delay:** Increase the delay for that application

### Can I add Steam games to EZ Streaming?
**Yes!** EZ Streaming can find Steam games automatically:
1. Use "Locate App by Name" and search for the game name
2. EZ Streaming will search your Steam library
3. It finds the game executable directly (not Steam.exe)

### How do I add browser bookmarks or websites?
**Current limitation:** EZ Streaming launches executables, not URLs directly.  
**Workaround:** Create a browser shortcut that opens to a specific URL, then add that shortcut to EZ Streaming.

## Timing and Performance

### What launch delays should I use?
**Recommended starting points:**
- **High-end systems:** 3-5 seconds default
- **Standard systems:** 5-7 seconds default  
- **Budget systems:** 8-12 seconds default

**Per-application recommendations:**
- **OBS/Streamlabs:** 8-12 seconds
- **Games:** 10-15 seconds
- **Discord/Spotify:** 2-5 seconds

### My system freezes when launching multiple applications. What should I do?
**System freezing indicates insufficient resources:**
1. **Increase launch delays** by 50-100%
2. **Reduce applications** in the profile
3. **Close background programs** before launching
4. **Consider hardware upgrade** if problem persists

### How do I optimize launch times?
**Optimization strategies:**
- **SSD storage:** Significantly faster than HDD
- **More RAM:** Allows more applications to run simultaneously
- **Close background apps:** Free up system resources
- **Optimal ordering:** Launch heavy applications first, light applications last

## Troubleshooting

### EZ Streaming won't start. What should I do?
**Troubleshooting steps:**
1. **Run as administrator:** Right-click → Run as administrator
2. **Check antivirus:** Temporarily disable or whitelist EZ Streaming
3. **Download fresh copy:** Redownload from GitHub releases
4. **Check system requirements:** Ensure Windows 10/11 64-bit

### My configuration isn't saving. How do I fix this?
**Configuration issues:**
1. **Check folder permissions:** Ensure EZ Streaming can write to AppData
2. **Run as administrator:** May need elevated permissions
3. **Check disk space:** Ensure adequate free space
4. **Antivirus interference:** Whitelist the configuration folder

### Applications show as "Launched" but aren't actually running. Why?
**Process detection issues:**
1. **Check application path:** Verify the path is still correct
2. **Application updates:** Some updates change executable locations
3. **Restart EZ Streaming:** Refresh the process detection system
4. **Manual verification:** Check Task Manager to confirm application status

### How do I reset EZ Streaming to default settings?
**To reset configuration:**
1. **Close EZ Streaming**
2. **Navigate to:** `C:\Users\[Username]\AppData\Roaming\EZStreaming\`
3. **Delete or rename:** `ez_streaming_config.json`
4. **Restart EZ Streaming:** It will create a new default configuration

## Advanced Usage

### Can I use EZ Streaming for non-streaming applications?
**Absolutely!** While designed for streamers, EZ Streaming works great for any scenario where you regularly launch the same set of applications:
- **Work setup:** IDE + Browser + Communication tools
- **Gaming:** Game + Discord + Music + Monitoring tools
- **Creative work:** Design software + Reference materials + Music

### Is there a command-line interface?
**Not currently.** EZ Streaming is designed as a GUI application. Command-line support may be added in future versions based on user demand.

### Can I run multiple instances of EZ Streaming?
**Not recommended.** Multiple instances can cause configuration conflicts. Use profiles instead to manage different application sets.

### How do I backup my profiles?
**Manual backup:**
1. Navigate to `C:\Users\[Username]\AppData\Roaming\EZStreaming\`
2. Copy `ez_streaming_config.json` to a safe location
3. **Built-in backup/export features** are planned for future releases

## Future Features

### What new features are planned?
**Upcoming features include:**
- Profile import/export functionality
- Auto-save capabilities
- Windows startup integration
- Command-line argument support for launched applications
- Built-in settings panel
- Cross-platform support (macOS, Linux)

### How can I request a new feature?
**Feature requests are welcome:**
1. **Check existing requests** on GitHub Discussions
2. **Submit new ideas** via GitHub Issues
3. **Join the community** discussion about features
4. **Contribute code** if you're a developer

### Will EZ Streaming remain free?
**Yes, absolutely.** EZ Streaming will always remain free and open-source. Our commitment:
- No premium versions or paid features
- No subscriptions or recurring costs
- No data collection or monetization
- Open-source forever

## Getting Help

### Where can I get support?
**Support options:**
- **GitHub Issues:** For bugs and technical problems
- **GitHub Discussions:** For questions and community help
- **Documentation:** Comprehensive guides in the wiki
- **Email:** Contact the developer directly for urgent issues

### How do I report a bug?
**Bug reporting:**
1. **Check existing issues** to avoid duplicates
2. **Gather information:** System specs, EZ Streaming version, steps to reproduce
3. **Submit detailed report** on GitHub Issues
4. **Include screenshots** if applicable

### Can I contribute to EZ Streaming?
**Contributions are welcome!**
- **Code contributions:** Submit pull requests on GitHub
- **Documentation:** Help improve guides and documentation
- **Testing:** Test new features and report issues
- **Feedback:** Share your experience and suggestions

### Where can I find more detailed documentation?
**Documentation resources:**
- **Wiki:** Comprehensive guides on GitHub
- **Installation Guide:** Step-by-step setup instructions
- **User Guides:** Detailed feature explanations
- **Architecture:** Technical documentation for developers

## Community and Support

### Is there a user community?
**Growing community:**
- **GitHub Discussions:** Active community discussions
- **GitHub Issues:** Technical support and bug reports
- **Social Media:** Follow updates on Twitter
- **Email:** Direct contact with the developer

### How can I support the project?
**Ways to support:**
- **Star the project** on GitHub
- **Share with other streamers** and content creators
- **Report bugs** and provide feedback
- **Contribute code** or documentation
- **Buy the developer a coffee** (optional donation)

### What's the project's philosophy?
**Core principles:**
- **Free forever:** No premium features or subscriptions
- **User-focused:** Built for real streamer needs
- **Community-driven:** Features based on user feedback
- **Open and transparent:** Open-source development
- **Quality over quantity:** Polished, reliable features

---

## Still Have Questions?

If you can't find the answer to your question here:

1. **Search the [GitHub Issues](https://github.com/Dkmariolink/ez-streaming/issues)** - your question might already be answered
2. **Check [GitHub Discussions](https://github.com/Dkmariolink/ez-streaming/discussions)** for community Q&A
3. **Read the detailed guides** in our documentation wiki
4. **Submit a new question** if you can't find existing answers

**Remember:** No question is too basic! The community is friendly and helpful to users of all experience levels.
