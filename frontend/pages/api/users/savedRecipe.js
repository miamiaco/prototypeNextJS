import dbConnect from '../../../src/utils/dbConnect';
import User from '../../../src/models/user';
import Recipe from '../../../src/models/recipe';

export default async function handler(req, res) {
  await dbConnect();

  if (req.method === 'POST') {
    try {
      const { userId, recipeId, category } = req.body;

      const recipe = await Recipe.findById(recipeId);
      if (!recipe) {
        return res.status(404).json({ error: 'Recipe not found' });
      }

      const user = await User.findById(userId);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      const isDuplicate = user.savedRecipes.some(savedRecipe =>
        savedRecipe.recipeId.equals(recipeId) && savedRecipe.category === category
      );

      if (isDuplicate) {
        return res.status(400).json({ error: 'Recipe already saved in this category' });
      }

      user.savedRecipes.push({ recipeId, category });
      await user.save();

      res.status(200).json({ message: 'Recipe saved successfully' });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }

  } else if (req.method === 'GET') {
    const userId = req.headers['x-user-id']
    try {
      const user = await User.findById(userId)
      .populate({
        path: 'savedRecipes.recipeId',
        model: 'Recipe',

      });

      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      // Filter out any saved recipes where the recipeId is null (indicating the recipe no longer exists)
      const validSavedRecipes = user.savedRecipes.filter(({ recipeId }) => recipeId !== null);

      // Map over the filtered list to construct the response
      const savedRecipes = validSavedRecipes.map(({ recipeId, category }) => ({
        title: recipeId.title,
        content: recipeId.content,
        images: recipeId.images,
        url: recipeId.url,
        category,
        owner: recipeId.owner,
        _id: recipeId._id
      }));

      res.status(200).json(savedRecipes);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else if (req.method === 'DELETE') {
    const userId = req.headers['x-user-id']
    const recipeId = req.headers['x-recipe-id']


    try {
      const user = await User.findById(userId);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      // Remove the recipe from savedRecipes array
      const initialLength = user.savedRecipes.length;
      user.savedRecipes = user.savedRecipes.filter(savedRecipe => !savedRecipe.recipeId.equals(recipeId));

      if (initialLength === user.savedRecipes.length) {
        return res.status(404).json({ error: 'Recipe not found in saved list' });
      }

      await user.save();
      res.status(200).json({ message: 'Recipe removed successfully' });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.setHeader('Allow', ['POST', 'GET', 'DELETE']);
    res.status(405).end('Method Not Allowed');
  }
}