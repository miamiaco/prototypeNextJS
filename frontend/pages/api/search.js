import dbConnect from '../../src/utils/dbConnect';
import Recipe from '../../src/models/recipe';

export default async function handler(req, res) {
  const { query } = req.query;

  if (!query) {
    return res.status(400).json({ error: 'A query parameter is required.' });
  }

  await dbConnect();

  // Performs the search query
  const results = await Recipe.aggregate([
    {
      $search: {
        index: 'default',
        text: {
          query: query,
          path: ['title', 'content', 'owner'],
        }
      }
    },
    {
      $limit: 500
    },
    {
      $project: { title: 1, description: 1, images: 1, owner: 1 }
    }
  ]);

  res.status(200).json(results);
}
