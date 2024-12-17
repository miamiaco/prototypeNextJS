import mongoose from 'mongoose';


const recipeSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  content: {
    type: String,
    required: true
  },
  images: {
    type: [String],
    required: true
  },
  url: {
    type: String,
    required: true
  },
  category: {
    type: [String],
    required: false
  },
  owner: {
    type: String,
    required: false
  }
});

const Recipe = mongoose.models.Recipe || mongoose.model('Recipe', recipeSchema);

export default Recipe;



