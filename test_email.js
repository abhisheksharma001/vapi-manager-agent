const nodemailer = require('nodemailer');

async function sendTestEmail() {
    const transporter = nodemailer.createTransport({
        host: "smtp.gmail.com",
        port: 587,
        secure: false, // true for 465, false for other ports
        auth: {
            user: "taruner420@gmail.com",
            pass: "gujm srls cwam jbza",
        },
    });

    const mailOptions = {
        from: '"Vox Manager Agent" <taruner420@gmail.com>',
        to: "taruner420@gmail.com",
        subject: "OpenClaw Manager Agent: Live Test Report",
        text: "Hi Abhi, this is a live test from your Manager Agent POC. If you see this, my email tool is working via the custom script.",
        html: "<b>Hi Abhi</b>,<br><br>This is a live test from your <b>Manager Agent POC</b>. If you see this, my email tool is working via the custom script. ⚡",
    };

    try {
        let info = await transporter.sendMail(mailOptions);
        console.log("Email sent successfully: " + info.messageId);
    } catch (error) {
        console.error("Error sending email: " + error.message);
    }
}

sendTestEmail();
