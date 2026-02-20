const nodemailer = require('nodemailer');

async function sendTestEmail() {
    console.log("Starting email test with Port 465 (SSL)...");
    const transporter = nodemailer.createTransport({
        host: "smtp.gmail.com",
        port: 465,
        secure: true, // true for 465
        auth: {
            user: "taruner420@gmail.com",
            pass: "gujm srls cwam jbza",
        },
        debug: true, // Show detailed logs
        logger: true // Log information to console
    });

    const mailOptions = {
        from: '"Vox Manager Agent" <taruner420@gmail.com>',
        to: "taruner420@gmail.com",
        subject: "OpenClaw Manager Agent: Live Test (Port 465)",
        text: "Hi Abhi, testing Port 465 to bypass potential security blocks.",
        html: "<b>Hi Abhi</b>,<br><br>Testing Port 465 to bypass potential security blocks. ⚡",
    };

    try {
        let info = await transporter.sendMail(mailOptions);
        console.log("SUCCESS! Email sent: " + info.messageId);
    } catch (error) {
        console.error("FAILED! Error details: " + error.message);
        if (error.message.includes("535")) {
            console.log("\nPossible root cause: Google login rejected. Please check for a 'Sign-in blocked' email from Google or verify your App Password.");
        }
    }
}

sendTestEmail();
