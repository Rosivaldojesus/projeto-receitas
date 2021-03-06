from urllib import response

from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewTest(TestCase):

    def setUp(self) -> None:

        category = Category.objects.create(name='category')
        author = User.objects.create(
            first_name='user',
            last_name='name',
            username='username',
            password='12345',
            email='username@email.com',
        )
        recipe = Recipe.objects.create(
            category = category,
            author = author,
            title = 'Recipe title',
            description = 'Recipe description',
            slug = 'recipe-slug',
            preparation_time = 10,
            preparation_time_unit ='Minutos', 
            servings = 5,
            servings_unit ='Porções', 
            preparation_steps = 'Recipe preparation steps',
            preparation_steps_is_html = True,
            is_published=True,
        )

        return super().setUp()



    def tearDown(self) -> None:
        return super().tearDown()




    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    
    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        


    def test_recipe_home_view_loads_correct_templates(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')


    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        Recipe.objects.get(pk=1).delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipe found here :)',
            response.content.decode('utf-8')
        )




    def test_recipe_home_template_loads_recipes(self):
        
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_recipes = response.context['recipes']

        self.assertEqual(len(response.context['recipes']), 1)
        self.assertEqual(response_recipes.first().title, 'Recipe title')

        self.assertIn('Recipe title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)



    
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_status_code_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)


    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_status_code_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)


    

