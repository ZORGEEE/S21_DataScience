from collections import defaultdict
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pytest
import sys
import re

class MovieLens():
    """Оберточный класс"""
    def __init__(self, file_path):
        try:
            if file_path == "data/links.csv":
                self.links = Links(file_path)
            elif file_path == "data/movies.csv":
                self.movies = Movies(file_path)
            elif file_path == "data/ratings.csv":
                self.ratings = Ratings(file_path)
                self.ratings_movies = self.ratings.Movies(self.ratings.ratings_data, self.ratings.movies_path)
                self.ratings_users = self.ratings.Users(self.ratings.ratings_data)
            elif file_path == "data/tags.csv":
                self.tags = Tags(file_path)
        except Exception as e:
            print(f"{e}")

class Links:
    def __init__(self, path_to_the_file):
        self.data = self.load_links_file(path_to_the_file)
        self.imdb = dict()

    def load_links_file(self, path) -> list:
        try:
            with open(path, 'r') as f:
                next(f)

                data = {}

                for line in f:
                    data.update(self.load_links(line))

                return data
        except:
            raise Exception('Invalid file')

    def load_links(self, line) -> dict:
        movieId, imdbId, tmdbId = line.strip().split(',')

        return {
            int(movieId) : {
                'imdbId': imdbId,
                'tmdbId': tmdbId
            }
        }
    
    def check_response(self, url):
        headers = {
        "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f'Connection error. Status code: {response.status_code}')

        return response
    
    def get_title(self, soup) -> str:
        title = soup.find('h1').text.strip()

        return title
    
    def get_director(self, soup) -> str:
        director = soup.select_one('a.ipc-metadata-list-item__list-content-item').text.strip()

        return director
    
    def get_budget(self, soup) -> str:
        budget = soup.find(string='Budget').find_next('span').text.strip().split()[0]

        return budget

    def get_gross(self, soup) -> str:
        gross = soup.find(string='Gross worldwide').find_next('span').text.strip()

        return gross
    
    def get_runtime(self, soup) -> str:
        runtime = soup.find(string='Runtime').find_next('div').text.strip()

        return runtime

    def get_rating(self, soup) -> str:
        rating = (soup.select_one('div[data-testid="hero-rating-bar__aggregate-rating__score"]').text).split('/')

        return rating[0]
    
    def get_imdb(self, list_of_movies, list_of_fields) -> dict:
        """
        Метод возвращает словарь словарей {movieId : { Director : str, Budget : '$', Runtime : hour/minute, ...} для списка фильмов, 
        заданного в качестве аргумента (movieId).
        Пример list_of_field - [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        Отсортируйте по убыванию по movieId.
        Пример: links.get_imdb([1, 2, 3], ['Rating', 'Budget'])
        """
        imdb_info = {movieId : {} for movieId in list_of_movies}

        for movieId in list_of_movies:
            if movieId not in self.data:
                raise KeyError(f'MovieId {movieId} not found')
            
            url = f'https://www.imdb.com/title/tt{self.data[movieId]['imdbId']}' 
            response = self.check_response(url)

            soup = BeautifulSoup(response.text, 'html.parser')


            imdb_info[movieId]['Title'] = self.get_title(soup)

            for fields in list_of_fields:
                if fields == 'Director':
                    imdb_info[movieId]['Director'] = self.get_director(soup)
                elif fields == 'Budget':
                    imdb_info[movieId]['Budget'] = self.get_budget(soup)
                elif fields == 'Cumulative Worldwide Gross':
                    imdb_info[movieId]['Cumulative Worldwide Gross'] = self.get_gross(soup)
                elif fields == 'Runtime':
                    imdb_info[movieId]['Runtime'] = self.get_runtime(soup)
                elif fields == 'Rating':
                    imdb_info[movieId]['Rating'] = self.get_rating(soup)

        self.imdb = imdb_info
        return imdb_info
        
    def top_directors(self, n) -> dict:
        """
        Метод возвращает dict с топ-n режиссеров, где ключами являются режиссеры, а 
        значения - номера фильмов, созданных ими. Отсортируйте его по номерам по убыванию.
        """
        try:
            directors = dict(
                sorted(
                    ((info['Director'], movieId) for movieId, info in self.imdb.items()),
                    key=lambda x: x[1],
                    reverse=True
                )[:n]
            )
        except: 
            raise KeyError('The Director\'s field was not requested')


        return directors
        
    def most_expensive(self, n) -> dict:
        """
        Метод возвращает дикту с топ-n фильмов, где ключами являются названия фильмов, а
        значения - их бюджеты. Сортировка по бюджету по убыванию.
        """
        try:
            budgets = dict(
                sorted(
                    ((info['Title'], info['Budget']) for info in self.imdb.values()),
                    key=lambda x: self.money_to_int(x[1]),
                    reverse=True
                )[:n]
            )
        except: 
            raise KeyError('The Budget\'s field was not requested')

        return budgets
    
    def money_to_int(self, money):
        return int(money.replace('$', '').replace(',', ''))

    def money_to_str(self, money):
        return f"${money:,}"
    
    def most_profitable_help(self, budget, gross) -> str:
        gross = self.money_to_int(gross)
        budget = self.money_to_int(budget)
        return self.money_to_str(gross - budget)
        
    def most_profitable(self, n) -> dict:
        """
        Метод возвращает дикту с топ-n фильмов, где ключами являются названия фильмов, а
        значения - разница между совокупным мировым валовым сбором и бюджетом.
        Сортировка по разнице по убыванию.
        """
        try:
            profits = dict(
                sorted(
                ((info['Title'], self.most_profitable_help(info['Budget'], info['Cumulative Worldwide Gross'])) for info in self.imdb.values()),
                key=lambda x: self.money_to_int(x[1]),
                reverse=True
                )[:n]
            )
        except: 
            raise KeyError('The Budget\'s or Cumulative Worldwide Gross field was not requested')
        
        return profits
        
    def time_in_minute(self, runtime) -> int:
        runtime_format = runtime.split()

        minutes = 0

        if 'hour' in runtime_format or 'hours' in runtime_format:
            minutes += int(runtime_format[0]) * 60

        if 'minutes' in runtime_format:
            index_m = runtime_format.index('minutes')
            minutes += int(runtime_format[index_m - 1])

        return minutes

    def longest(self, n) -> dict:
        """
        Метод возвращает дикту с топ-n фильмов, где ключами являются названия фильмов, а
        значения - время их показа. Если есть несколько версий - выберите любую.
        Сортировка по времени выполнения по убыванию.
        """
        try:
            runtimes_dict = {info['Title'] : info['Runtime'] for info in self.imdb.values()}

            runtimes = dict(
                sorted(
                    runtimes_dict.items(),
                    key=lambda x: self.time_in_minute(x[1]),
                    reverse=True
                )[:n]
            )
        except:
            raise KeyError('The Runtime\'s field was not requested')

        return runtimes
    
    def top_cost_per_minute_help(self, budget, runtime) -> float:
        budget = self.money_to_int(budget)
        runtime = self.time_in_minute(runtime)

        round_result = round(budget / runtime, 2)

        return round_result
        
    def top_cost_per_minute(self, n) -> dict:
        """
        Метод возвращает дикту с топ-n фильмов, где ключами являются названия фильмов, а 
        значения - бюджеты, разделенные на время их показа. 
        Бюджеты могут быть в разных валютах - не обращайте на это внимания. 
        Значения должны быть округлены до 2 знаков после запятой. Отсортируйте их по убыванию деления.
        """
        try:
            costs_dict = {info['Title'] : self.top_cost_per_minute_help(info['Budget'], info['Runtime'])for info in self.imdb.values()}

            costs = dict(
                sorted(
                    costs_dict.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:n]
            )
        except:
            raise KeyError('The Budget or Runtime field was not requested')

        return costs
    
    def efficiency_score_help(self, rating, budget) -> float:
        rating = float(rating)
        budget = self.money_to_int(budget)
        
        # Вычисляем натуральный логарифм через ряд Тейлора (для budget > 0)
        
        
        ln_budget = Statistics._natural_log(budget)
        return round(rating ** 2 / ln_budget, 2)
    
    def top_efficiency_score(self, n) -> dict:
        """
        Метод возвращает словарь с топ-n фильмаов по формуле эффективности,
        (rating**2 / log(budget) - формула была придумана.
        Значения округлены до 2 знаков после запятой. Отсортированы в порядке убывания.
        """
        try:
            efficiency_dict = {info['Title'] : self.efficiency_score_help(info['Rating'], info['Budget']) for info in self.imdb.values()}

            efficiency = dict(
                sorted(
                    efficiency_dict.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:n]
            )
        except:
            raise KeyError('The Rating or Budget field was not requested')
        return efficiency

class Movies:
    def __init__(self, path_to_the_file):
        self.movies_data = self.load_movies_file(path_to_the_file)
    
    def load_movies_file(self, path) -> list:
        try:
            with open(path, 'r') as f:
                next(f)
                return [self.load_movies(f)]
        except Exception as e:
            print(f"{e}")

    def load_movies(self, f) -> dict:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 3:
                continue
            movie_id = int(parts[0])                
            title = ','.join(parts[1:-1])  # объединяем части названия с запятыми
            year = re.search(r'\((\d{4})\)$', title)
            genres = parts[-1]
            return {
                'movieId': movie_id,
                'title': title,
                'year': int(year.group(1)) if year else None,
                'genres': genres.split('|')
            }

    def dist_by_release(self):
        """
        Returns {year: count} sorted by counts descending
        """
        year_counts = defaultdict(int)
        for movie in self.movies_data:
            if movie['year']:
                year_counts[movie['year']] += 1
        return dict(sorted(year_counts.items(), key=lambda x: (-x[1], x[0])))

    def dist_by_genres(self):
        """
        Returns {genre: count} sorted by counts descending
        """
        genre_counts = defaultdict(int)
        for movie in self.movies_data:
            for genre in movie['genres']:
                genre_counts[genre] += 1
        return dict(sorted(genre_counts.items(), key=lambda x: (-x[1], x[0])))

    def most_genres(self, n):
        """
        Returns {title: num_genres} for top-n movies sorted by num_genres descending
        """
        movies_with_counts = {
            movie['title']: len(movie['genres'])
            for movie in self.movies_data
        }
        return dict(sorted(
            movies_with_counts.items(),
            key=lambda x: (-x[1], x[0])
        )[:n])
    
    def decade_analysis(self):
        """
        Распределение фильмов по десятилетиям.
        Формат: {'1990-1999': X, '2000-2009': Y}
        """
        decade_counts = defaultdict(int)
        for movie in self.movies_data:
            if movie['year']:
                decade = f"{movie['year'] // 10 * 10}-{(movie['year'] // 10 * 10) + 9}"
                decade_counts[decade] += 1
        return dict(sorted(decade_counts.items(), key=lambda x: -x[1]))

    def genre_combinations(self, top_n: int):
        """
        Самые популярные комбинации жанров.
        Формат: {'Action|Adventure': X, 'Comedy|Romance': Y}
        """
        comb_counts = defaultdict(int)
        for movie in self.movies_data:
            if len(movie['genres']) >= 2:
                key = '|'.join(sorted(movie['genres']))
                comb_counts[key] += 1
        return dict(sorted(comb_counts.items(), key=lambda x: -x[1])[:top_n])

    def longest_title(self, n: int):
        """
        Фильмы с самыми длинными названиями.
        Формат: {название: длина_названия}
        """
        titles = {
            movie['title']: len(movie['title'])
            for movie in self.movies_data
        }
        return dict(sorted(titles.items(), key=lambda x: -x[1])[:n])

class Ratings:
    def __init__(self, ratings_path):
        self.ratings_data = self._load_ratings(ratings_path)
        self.movies_path = "data/movies.csv"
    
    def _load_ratings(self, path):
        try:
            with open(path, 'r') as f:
                next(f)  # Skip header
                return [self._parse_rating(line) for line in f]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def _parse_rating(self, line):
        parts = line.strip().split(',')
        return {
            'userId': int(parts[0]),
            'movieId': int(parts[1]),
            'rating': float(parts[2]),
            'timestamp': int(parts[3])
        }

    class Movies:
        def __init__(self, ratings_data, movies_path):
            self.movies_data = self._load_movies(movies_path)
            self.ratings_by_movie = self._group_ratings_by_movie(ratings_data)
        
        def _group_ratings_by_movie(self, ratings_data):
            ratings_by_movie = defaultdict(list)
            for rating in ratings_data:
                ratings_by_movie[rating['movieId']].append(rating['rating'])
            return ratings_by_movie

        def _load_movies(self, path):
            movies = {}
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    next(f)  # Skip header
                    for line in f:
                        movie = self._parse_movie_line(line)
                        if movie:
                            movies[movie['movieId']] = movie
                return movies
            except Exception as e:
                print(f"Error: {e}")
                return {}

        def _parse_movie_line(self, line):
            parts = line.strip().split(',', 2)  # Split into 3 parts
            if len(parts) != 3:
                return None
            movie_id_str, title, genres = parts
            try:
                movie_id = int(movie_id_str)
            except ValueError:
                return None
            year_match = re.search(r'\((\d{4})\)$', title.strip())
            year = int(year_match.group(1)) if year_match else None
            if year_match:
                title = title[:year_match.start()].strip()
            return {
                'movieId': movie_id,
                'title': title,
                'year': year,
                'genres': genres.split('|')
            }

        def dist_by_year(self):
            year_counts = defaultdict(int)
            for movie_id, ratings in self.ratings_by_movie.items():
                movie = self.movies_data.get(movie_id)
                if movie and movie['year'] is not None:
                    year_counts[movie['year']] += len(ratings)
            return dict(sorted(year_counts.items()))

        def dist_by_rating(self):
            rating_counts = defaultdict(int)
            for ratings in self.ratings_by_movie.values():
                for rating in ratings:
                    rating_counts[rating] += 1
            return dict(sorted(rating_counts.items()))

        def top_by_num_of_ratings(self, n):
            counts = {self.movies_data[m_id]['title']: len(ratings) 
                      for m_id, ratings in self.ratings_by_movie.items() 
                      if m_id in self.movies_data}
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            return dict(sorted_counts[:n])

        def top_by_ratings(self, n, metric="mean"):
            metrics = {}
            for m_id, ratings in self.ratings_by_movie.items():
                if not ratings:
                    continue
                movie_title = self.movies_data.get(m_id, {}).get('title', 'Unknown')
                val = round(Statistics._mean(ratings), 2)
                metrics[movie_title] = val
            sorted_metrics = sorted(metrics.items(), key=lambda x: (-x[1], x[0]))
            return dict(sorted_metrics[:n])

        def top_controversial(self, n):
            variances = {}
            for m_id, ratings in self.ratings_by_movie.items():
                if len(ratings) < 2:
                    var = 0.0
                else:
                    var = Statistics._variance(ratings)
                movie_title = self.movies_data.get(m_id, {}).get('title', 'Unknown')
                variances[movie_title] = round(var, 2)
            sorted_variances = sorted(variances.items(), key=lambda x: (-x[1], x[0]))
            return dict(sorted_variances[:n])
    
        def year_with_most_ratings(self):
            """
            Возвращает год с наибольшим количеством оценок.
            Формат: (год, количество)
            """
            year_counts = self.dist_by_year()
            if not year_counts:
                return (None, 0)
            max_year = max(year_counts.items(), key=lambda x: x[1])
            return max_year

    class Users(Movies):
        def __init__(self, ratings_data):
            self.ratings_data = ratings_data

        def dist_by_num_of_ratings(self):
            user_counts = defaultdict(int)
            for rating in self.ratings_data:
                user_counts[rating['userId']] += 1

            rating_dist = defaultdict(int)
            for count in user_counts.values():
                rating_dist[count] += 1

            return dict(sorted(rating_dist.items()))

        def dist_by_ratings(self, metric='average'):
            user_ratings = defaultdict(list)
            for rating in self.ratings_data:
                user_ratings[rating['userId']].append(rating['rating'])

            metric_func = Statistics._mean if metric == 'average' else Statistics._median
            rating_dist = defaultdict(int)
            for _, ratings in user_ratings.items():
                avg = round(metric_func(ratings), 2)
                rating_dist[avg] += 1

            return dict(sorted(rating_dist.items(), key=lambda x: x[0]))

        def top_by_variance(self, n):
            user_ratings = defaultdict(list)
            for rating in self.ratings_data:
                user_ratings[rating['userId']].append(rating['rating'])

            user_variance = {}
            for user, ratings in user_ratings.items():
                if len(ratings) >= 2:
                    user_variance[user] = round(Statistics._variance(ratings), 2)

            sorted_users = sorted(user_variance.items(), key=lambda x: (-x[1], x[0]))
            return dict(sorted_users[:n])
        
        def most_active_in_period(self, start_year: int, end_year: int):
            """
            Самые активные пользователи в указанный период.
            Формат: {userId: количество_оценок}
            """
            period_data = [
                r for r in self.ratings_data
                if start_year <= datetime.fromtimestamp(r['timestamp']).year <= end_year
            ]
            user_counts = defaultdict(int)
            for rating in period_data:
                user_counts[rating['userId']] += 1
            return dict(sorted(user_counts.items(), key=lambda x: -x[1]))

        def compare_generous_vs_strict(self):
            """
            Сравнение количества "щедрых" (avg >=4) и "строгих" (avg <=2) пользователей.
            Формат: {'generous': X, 'strict': Y}
            """
            rating_dist = self.dist_by_ratings()
            generous = sum(v for k, v in rating_dist.items() if k >= 4)
            strict = sum(v for k, v in rating_dist.items() if k <= 2)
            return {'generous': generous, 'strict': strict}

class Tags:
    def __init__(self, path_to_the_file):
        self.data = self.load_tags_file(path_to_the_file)

    def load_tags_file(self, path) -> list:
        try:
            with open(path, 'r') as f:
                next(f)
                return [self.load_tags(line) for line in f]
        except:
            raise Exception('Invalid fail')

    def load_tags(self, line) -> dict:
        userId, movieId, tag, timestamp = line.strip().split(',')

        return {
            'userID': int(userId),
            'movieId' : movieId,
            'tag' : tag,
            'timestamp' : timestamp
        }

    def most_words(self, n) -> list:
        """
        Метод возвращает топ-n тегов с наибольшим количеством слов внутри. Он представляет собой дикту 
        где ключами являются теги, а значениями - количество слов внутри тега.
        Отбросьте дубликаты. Отсортируйте по убыванию.
        """
        tags_dict = {item['tag'] : len(item['tag'].split(' ')) for item in self.data}

        big_tags = sorted(tags_dict.items(), key=lambda x: x[1], reverse=True)

        return big_tags[:n]

    def longest(self, n) -> list:
        """
        Метод возвращает топ-n самых длинных тегов по количеству символов.
        Это список тегов. Отбросьте дубликаты. Отсортируйте его по убыванию номеров.
        """
        tags_list = list(dict.fromkeys(item['tag'] for item in self.data))
        

        big_tags = sorted(tags_list, key=lambda x: len(x), reverse=True)

        return big_tags[:n]

    def most_words_and_longest(self, n) -> list:
        """
        Метод возвращает пересечение между топ-n тегов с наибольшим количеством слов внутри и 
        топ-n самых длинных тегов по количеству символов.
        Отбросьте дубликаты. Это список тегов.
        """
        most_words_list = [tag[0] for tag in self.most_words(n)]
        longest_list = self.longest(n)

        big_tags = list(set(most_words_list) & set(longest_list))

        return big_tags
        
    def most_popular(self, n) -> dict:
        """
        Метод возвращает наиболее популярные теги. 
        Это диктант, в котором ключами являются теги, а значениями - их количество.
        Отбросьте дубликаты. Отсортируйте по убыванию.
        """
        tags_count = {}

        for line in self.data:
            tag = line['tag']
            tags_count[tag] = tags_count.get(tag, 0) + 1

        popular_tags = dict(
            sorted(
                tags_count.items(), 
                key=lambda x: x[1], 
                reverse=True
                )[:n]
            ) # {'tags' : count}

        return popular_tags
        
    def tags_with(self, word) -> list: 
        """
        Метод возвращает все уникальные теги, включающие слово, заданное в качестве аргумента.
        Отбросьте дубликаты. Это список тегов. Отсортируйте его по названиям тегов в алфавитном порядке.
        """
        tags_with_word = sorted(list(set(item['tag'] for item in self.data if word in item['tag'].split())))

        return tags_with_word
    
    def tags_uniq(self):
        """
        Метод возвращает процент уникальных тегов от общего количества тегов
        """
        all_tags = [item['tag'] for item in self.data]
        uniq_tags = set(all_tags)
    
        return round(len(uniq_tags) / len(all_tags) * 100, 2)

class Statistics:
    @staticmethod
    def _mean(ratings):
         """Ручной расчет среднего"""
         return sum(ratings) / len(ratings) if ratings else 0

    @staticmethod
    def _median(ratings):
        """Ручной расчет медианы"""
        sorted_ratings = sorted(ratings)
        n = len(sorted_ratings)
        if n == 0:
            return 0
        elif n % 2 == 1:
            return sorted_ratings[n // 2]
        else:
            return (sorted_ratings[n // 2 - 1] + sorted_ratings[n // 2]) / 2

    @staticmethod
    def _variance(ratings):
        """Ручной расчет дисперсии"""
        if len(ratings) < 2:
            return 0
        mean = Statistics._mean(ratings)
        return sum((x - mean) ** 2 for x in ratings) / (len(ratings) - 1)
    
    @staticmethod
    def _natural_log(x):
        """Ручной расчет логорифма"""
        if x <= 0:
            return float('-inf')
        n = 1000  # Число итераций для точности
        result = 0.0
        for i in range(1, n + 1):
            term = (x - 1) ** i / (i * (x ** i)) if i % 2 == 1 else - (x - 1) ** i / (i * (x ** i))
            result += term
        return result

class Tests:
    class TestLinks:
        @pytest.fixture
        def sample_links(self):
            return Links('data/links.csv')

        def test_invalid_links_file(self):
            with pytest.raises(Exception):
                Links('data/links.cs')

        def test_invalid_url(self):
            with pytest.raises(Exception):
                Links.check_response('https://www.imdb.com/title/tt011093')

        def test_invalid_movieId(self, sample_links):
            with pytest.raises(KeyError):
                sample_links.get_imdb([200], ['Budget'])

        def test_get_imdb(self, sample_links):
            assert isinstance(sample_links.data, dict)
            assert len(sample_links.data) == 9742
            assert sample_links.get_imdb([1], ['Director']) == {1: {'Title': 'Toy Story', 'Director': 'John Lasseter'}}
            assert sample_links.get_imdb([1], ['Budget']) == {1: {'Title': 'Toy Story', 'Budget': '$30,000,000'}}
            assert sample_links.get_imdb([1], ['Cumulative Worldwide Gross']) == {1: {'Title': 'Toy Story', 'Cumulative Worldwide Gross': '$394,436,586'}}
            assert sample_links.get_imdb([1], ['Runtime']) == {1: {'Title': 'Toy Story', 'Runtime': '1 hour 21 minutes'}}
            assert sample_links.get_imdb([1], ['Rating']) == {1: {'Title': 'Toy Story', 'Rating': '8.3'}}

        def test_top_directors(self):
            links = Links('data/links.csv')
            links.get_imdb([1], ['Budget'])
            with pytest.raises(KeyError):
                links.top_directors(2)
                
            links.get_imdb([1, 2], ['Director'])
            directors = links.top_directors(3)
            assert directors == {'Joe Johnston': 2, 'John Lasseter': 1}


        def test_most_expensive(self):
            links = Links('data/links.csv')
            links.get_imdb([1], ['Director'])
            with pytest.raises(KeyError):
                links.most_expensive(2)

            links.get_imdb([1, 2], ['Budget'])
            budgets = links.most_expensive(2)
            assert budgets == {'Jumanji': '$65,000,000', 'Toy Story': '$30,000,000'}

        def test_most_profitable(self):
            links = Links('data/links.csv')
            links.get_imdb([1], ['Budget'])
            with pytest.raises(KeyError):
                links.most_profitable(2)
            
            links.get_imdb([1, 2], ['Budget', 'Cumulative Worldwide Gross'])
            profitable = links.most_profitable(3)
            assert profitable == {'Toy Story': '$364,436,586', 'Jumanji': '$197,821,940'}

        def test_longest(self):
            links = Links('data/links.csv')
            links.get_imdb([1], ['Budget'])
            with pytest.raises(KeyError):
                links.longest(2)
            
            links.get_imdb([1, 2], ['Runtime'])
            profitable = links.longest(3)
            assert profitable == {'Jumanji': '1 hour 44 minutes', 'Toy Story': '1 hour 21 minutes'}

        def test_longest(self):
            links = Links('data/links.csv')
            links.get_imdb([1], ['Budget'])
            with pytest.raises(KeyError):
                links.top_cost_per_minute(2)
            
            links.get_imdb([1, 2], ['Budget', 'Runtime'])
            profitable = links.top_cost_per_minute(3)
            assert profitable == {'Jumanji': 625000.0, 'Toy Story': 370370.37}

        def test_top_efficiency_score(self):
            links = Links('data/links.csv')
            links.get_imdb([1], ['Budget'])
            with pytest.raises(KeyError):
                links.top_efficiency_score(2)
            
            links.get_imdb([1, 2], ['Budget', 'Rating'])
            profitable = links.top_efficiency_score(3)

    class TestRatingsMovies:
        @pytest.fixture
        def sample_ratings(self):
            return Ratings("data/ratings.csv")

        def test_dist_by_year(self, sample_ratings):
            movies = sample_ratings.Movies(sample_ratings.ratings_data, sample_ratings.movies_path)
            result = movies.dist_by_year()
            assert isinstance(result, dict)
            for year, count in result.items():
                assert isinstance(year, int)
                assert isinstance(count, int)
            assert list(result.keys()) == sorted(result.keys())

        def test_dist_by_rating(self, sample_ratings):
            movies = sample_ratings.Movies(sample_ratings.ratings_data, sample_ratings.movies_path)
            result = movies.dist_by_rating()
            assert isinstance(result, dict)
            for rating, count in result.items():
                assert isinstance(rating, float)
                assert isinstance(count, int)
            assert list(result.keys()) == sorted(result.keys())

        def test_top_by_num_of_ratings(self, sample_ratings):
            movies = sample_ratings.Movies(sample_ratings.ratings_data, sample_ratings.movies_path)
            result = movies.top_by_num_of_ratings(3)
            assert isinstance(result, dict)
            items = list(result.items())
            sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))
            assert items == sorted_items

        def test_top_by_ratings(self, sample_ratings):
            movies = sample_ratings.Movies(sample_ratings.ratings_data, sample_ratings.movies_path)
            result = movies.top_by_ratings(3)
            assert isinstance(result, dict)
            items = list(result.items())
            sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))
            assert items == sorted_items

        def test_top_controversial(self, sample_ratings):
            movies = sample_ratings.Movies(sample_ratings.ratings_data, sample_ratings.movies_path)
            result = movies.top_controversial(2)
            assert isinstance(result, dict)
            items = list(result.items())
            sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))
            assert items == sorted_items

        def test_year_with_most_ratings(self, sample_ratings):
            movies = sample_ratings.Movies(sample_ratings.ratings_data, sample_ratings.movies_path)
            year, count = movies.year_with_most_ratings()
            assert isinstance(year, int) or year is None
            assert isinstance(count, int)

    class TestRatingsUsers:
        @pytest.fixture
        def sample_ratings(self):
            return Ratings("data/ratings.csv")

        def test_dist_by_num_of_ratings(self, sample_ratings):
            users = sample_ratings.Users(sample_ratings.ratings_data)
            result = users.dist_by_num_of_ratings()
            assert isinstance(result, dict)
            assert list(result.keys()) == sorted(result.keys())

        def test_dist_by_ratings(self, sample_ratings):
            users = sample_ratings.Users(sample_ratings.ratings_data)
            result = users.dist_by_ratings()
            assert isinstance(result, dict)
            assert list(result.keys()) == sorted(result.keys())

        def test_top_by_variance(self, sample_ratings):
            users = sample_ratings.Users(sample_ratings.ratings_data)
            result = users.top_by_variance(2)
            assert isinstance(result, dict)
            items = list(result.items())
            sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))
            assert items == sorted_items
        
        def test_most_active_in_period(self, sample_ratings):
            users = sample_ratings.Users(sample_ratings.ratings_data)
            result = users.most_active_in_period(2000, 2005)
            assert isinstance(result, dict)
            assert list(result.values()) == sorted(result.values(), reverse=True)

        def test_compare_generous_vs_strict(self, sample_ratings):
            users = sample_ratings.Users(sample_ratings.ratings_data)
            result = users.compare_generous_vs_strict()
            assert set(result.keys()) == {'generous', 'strict'}
            assert all(isinstance(v, int) for v in result.values())


    class TestMovies:
        @pytest.fixture
        def sample_movies(self):
            return Movies("data/movies.csv")

        def test_dist_by_release(self, sample_movies):
            result = sample_movies.dist_by_release()
            assert isinstance(result, dict)
            items = list(result.items())
            sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))
            assert items == sorted_items

        def test_dist_by_genres(self, sample_movies):
            result = sample_movies.dist_by_genres()
            assert isinstance(result, dict)
            items = list(result.items())
            sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))
            assert items == sorted_items

        def test_most_genres(self, sample_movies):
            result = sample_movies.most_genres(3)
            assert isinstance(result, dict)
            items = list(result.items())
            sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))
            assert items == sorted_items

        def test_decade_analysis(self, sample_movies):
            result = sample_movies.decade_analysis()
            assert isinstance(result, dict)
            for decade in result.keys():
                assert re.match(r"\d{4}-\d{4}", decade)

        def test_genre_combinations(self, sample_movies):
            result = sample_movies.genre_combinations(top_n=2)
            assert isinstance(result, dict)
            for combo in result.keys():
                assert '|' in combo

        def test_longest_title(self, sample_movies):
            result = sample_movies.longest_title(3)
            assert isinstance(result, dict)
            for title, length in result.items():
                assert isinstance(title, str)
                assert isinstance(length, int)

    class TestTags:
        @pytest.fixture
        def sample_tags(self):
            return Tags("data/tags.csv")

        def test_invalid_tags_file(self):
            with pytest.raises(Exception):
                Tags("data/tags.cs")

        def test_most_words(self, sample_tags):
            words = sample_tags.most_words(10)

            assert len(words) == 10
            assert words[0] == ('Something for everyone in this one... saw it without and plan on seeing it with kids!', 16)
            assert words[-1] == ('based on a true story', 5)

        def test_longest(self, sample_tags):
            longest = sample_tags.longest(10)

            assert len(longest) == 10
            assert longest[0] == 'Something for everyone in this one... saw it without and plan on seeing it with kids!'
            assert longest[-1] == 'It was melodramatic and kind of dumb'

        def test_most_words_and_longest(self, sample_tags):
            words_and_longest = sample_tags.most_words_and_longest(10)

            assert len(words_and_longest) == 7

        def test_most_popular(self, sample_tags):
            popular = sample_tags.most_popular(10)

            assert len(popular) == 10
            assert popular['funny'] == 23

        def test_tags_with(self, sample_tags):
            tags = sample_tags.tags_with('way')
            
            assert len(tags) == 1
            
            assert tags[-1] == 'way too long'

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        pytest.main([__file__])
