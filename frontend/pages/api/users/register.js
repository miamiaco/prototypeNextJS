import dbConnect from '../../../src/utils/dbConnect';
import User from '../../../src/models/user';
import bcrypt from 'bcrypt';

export default async function handler(req, res) {
  if (req.method === 'POST') {

    try {
      await dbConnect();

      const { username, name, password } = req.body;


      if (!password || password.length < 3) {
        return res.status(400).json({ error: 'password missing or too short' });
      }

      const hashedPassword = await bcrypt.hash(password, 10);

      const user = new User({
        username,
        name,
        password: hashedPassword,
      });

      const savedUser = await user.save();
      res.status(201).json(savedUser);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    // If the request is not a POST request, return 405 Method Not Allowed
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}