export default function handler(req, res) {
    // Clear the cookie
    res.setHeader('Set-Cookie', 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; httpOnly; sameSite=Lax');

    // Redirect to the homepage or login page after logout
    return res.status(200).json({ message: 'Logged out' });
  }
