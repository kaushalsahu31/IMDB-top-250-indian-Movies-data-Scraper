import requests, json, os, time, random

from bs4 import BeautifulSoup

from pprint import pprint


###########################    Task 1   ##############################



path="./imdb.json"
if os.path.exists(path):
	data=json.load(open("./imdb.json","r"))
	print(data)


else:
	url="https://www.imdb.com/india/top-rated-indian-movies/"
	data=requests.get(url).text
	soup=BeautifulSoup(data,"html.parser")
	tbody= soup.find("tbody", class_= "lister-list")
	trs=tbody.find_all("tr")
	movies=[]
	for i in trs:
		b={}
		data=i.find("td",class_="titleColumn")
		name=data.find("a").text
		url=data.find("a")["href"]
		b["name"]=name
		year=data.find("span",class_="secondaryInfo").text
		years=""
		q=year.index("(")
		w=year.index(")")
		for j in range(q+1,w):
			years+=year[j]
		b["year"] = int(years)
		rating=i.find("td" ,class_="ratingColumn imdbRating")
		rating=rating.find("strong").text
		b["rating"]=float(rating)
		b["url"]=("https://www.imdb.com"+url)
		position=i.find("td",class_="titleColumn").text.split('.')
		position=(position[0])
		b["position"]=int(position.strip())
		movies.append(b)
	file=open("imdb.json","w")
	filedata=json.dump(movies,file,indent=4)
	
	file.close()


###########################    Task 2   ##############################


path="./sort_by_year.json"
if os.path.exists(path):
	data=json.load(open("./sort_by_year.json","r"))
	print(data)

else:
	data=json.load(open("./imdb.json","r"))
	sortyear={}
	years=[]
	for i in data:
		if i["year"] not in years:
			years.append(i["year"])
	for i in years:
		year_data=[]
		for j in data:
			if  i==j["year"]:
				year_data.append(j)
		sortyear[i]=year_data
	file=open("sort_by_year.json","w")
	filedata=json.dump(sortyear,file,indent=4)
	file.close()



###########################    Task 3   ##############################



path="./sort_by_decade.json"
if os.path.exists(path):
	data=json.load(open("./sort_by_decade.json","r"))
	print(data)
else:
	data=json.load(open("./imdb.json","r"))
	decade=[]
	decadeslist={}
	for i in data:
		year=i["year"]-i['year']%10
		decade.append(year)
	decade=list(set(decade))
	decade.sort()
	for i in decade:
		decadelist=[]
		for j in data:
			if i<=j['year']<(i+10):
				decadelist.append(j)
		decadeslist[i]=decadelist
	file=open("sort_by_decade.json","w")
	filedata=json.dump(decadeslist,file,indent=3)
	file.close()		


###########################    Task 4   ##############################

path="./moviedetails.json"
if os.path.exists(path):
	file=json.load(open("moviedetails.json","r"))
	pprint(file)


else:

	file=json.load(open("imdb.json","r"))
	moviedetail=[]
	for i in file:
		ab=random.randint(1,4)
		url=i["url"]
		data=requests.get(url).text
		data=BeautifulSoup(data,"html.parser")
		namedata=data.find("div",class_="title_wrapper")
		a=namedata.find("h1").text
		details_of_movies={}
		index=a.index("(")
		name=""
		for i in range(index):
			name+=a[i]
		name=name.strip()
		details_of_movies["Name"]=name
		runtime=namedata.find("time").text
		details_of_movies["Time"]=(runtime.strip())
		genre=[]
		genres=namedata.find_all("a")
		for i in range(1,len(genres)-1):
			genre.append(genres[i].text)
		details_of_movies["Genre"]=(genre)
		biodata=data.find("div",class_="plot_summary")
		bio=biodata.find("div",class_="summary_text").text.strip()
		details_of_movies["Bio"]=(bio)
		directordetail=biodata.find("div",class_="credit_summary_item")
		director=directordetail.find_all("a")
		directors=[]
		for i in director:
			directors.append(i.text)
		details_of_movies["Director"]=(directors)
		countrydetail=data.find("div",id="titleDetails")
		countrydetail=countrydetail.find_all("div",class_="txt-block")
		if (countrydetail[0].find("h4").text)=="Country:":
			country=countrydetail[0].find("a").text
		else:
			country=countrydetail[1].find("a").text
		details_of_movies["Country"]=(country)
		if (countrydetail[1].find("h4").text)=="Language:":
			languages=countrydetail[1].find_all("a")
		else:
			languages=countrydetail[2].find_all("a")
		language=[]
		for i in languages:
			language.append(i.text)
		details_of_movies["Language"]=(language)
		postertag=data.find("div",class_="poster")
		poster=postertag.find("img")["src"]
		details_of_movies["Poster"]=(poster)
		moviedetail.append(details_of_movies)
		# print(details_of_movies)
		time.sleep(ab)


	file=open("moviedetails.json","w")
	filedata=json.dump(moviedetail,file,indent=4)
	file.close()


###########################    Task 5   ##############################


same task 4


###########################    Task 6   ##############################


path="./movies_by_language.json"
if os.path.exists(path):
	file=json.load(open("movies_by_language.json","r"))
	print(file)

else:	
	file=json.load(open("moviedetails.json","r"))
	movies_by_language={}
	languages=[]
	for i in file:
		language=i["Language"]
		for j in language:
			if j not in languages:
				languages.append(j)
	for i in languages:
		languagemovies=[]
		for j in file:
			if i in j["Language"]:
				languagemovies.append(j)
		movies_by_language[i]=len(languagemovies)
	file=open("movies_by_language.json","w")
	filedata=json.dump(movies_by_language,file,indent=4)
	file.close()


###########################    Task 7   ##############################


path="./movies_by_directors.json"
if os.path.exists(path):
	file=json.load(open("movies_by_directors.json","r"))
	print(file)

else:	
	file=json.load(open("moviedetails.json","r"))
	movies_by_directors={}
	directors=[]
	for i in file:
		director=i["Director"]
		for j in director:
			if j not in directors:
				directors.append(j)
	for i in directors:
		directormovies=[]
		for j in file:
			if i in j["Director"]:
				directormovies.append(j)
		movies_by_directors[i]=len(directormovies)
	file=open("movies_by_directors.json","w")
	filedata=json.dump(movies_by_directors,file,indent=4)
	file.close()


###########################    Task 8   ##############################


file=json.load(open("imdb.json","r"))
data=json.load(open("moviedetails.json","r"))
ab=0
for i in file:
	a=i["url"]
	a=a.split("/")
	a=a[-2]
	moviesdata=data[ab]
	filedata=open("task8/"+a+".json","w")
	datas=json.dump(moviesdata,filedata,indent=4)
	filedata.close()
	ab+=1


###########################    Task 9   ##############################


#####    Done in task4  ######


###########################    Task 10   ##############################


directorslist=[]
directorsdict={}
file=json.load(open("moviedetails.json","r"))
for i in file:
	director=i["Director"]
	for j in director:
		if j not in directorslist:
			directorslist.append(j)
for i in directorslist:
	languages=[]
	for j in file:
		if i in j["Director"]:
			language=j["Language"]
			for k in language:
				languages.append(k)
	languages_data=[]
	for a in languages:
		if a not in languages_data:
			languages_data.append(a)
	languages_data_dict={}
	for ij in languages_data:
		abc=0
		for jk in languages:
			if ij==jk:
				abc+=1
		languages_data_dict[ij]=abc

	directorsdict[i]=languages_data_dict
print(directorsdict)


###########################    Task 11   ##############################


genre=[]
genres=[]
genre_dict={}
file=json.load(open("moviedetails.json","r"))
for i in file:
	a=i["Genre"]
	for j in a:
		genre.append(j)
for i in genre:
	if i not in genres:
		genres.append(i)
for i in genres:
	count=0
	for j in genre:
		if i==j:
			count+=1
	genre_dict[i]=count
print(genre_dict)


###########################    Task 12   ##############################


path="./movie_id.json"
if os.path.exists(path):
	file=json.load(open("movie_id.json","r"))
	print(file)

else:
	files=json.load(open("imdb.json","r"))
	all_movies_id=[]
	for j in files:
		a=random.randint(1,3)
		id_data=[]
		file=j
		file=file["url"]
		file=file+"fullcredits?ref_=tt_cl_sm#cast"
		datas=requests.get(file).text
		soup=BeautifulSoup(datas,"html.parser")
		castdata=soup.find("table",class_="cast_list")
		cast=castdata.find_all("td",class_=False)
		for i in cast:
			cast={}
			ids=i.find("a")["href"]
			ids=ids.split("/")
			ids=ids[2]
			names=(i.text).strip()
			cast["id"]=ids
			cast["Names"]=names
			id_data.append(cast)
		all_movies_id.append(id_data)
		time.sleep(a)
	movie_id=open("movie_id.json","w")
	moviesdata=json.dump(all_movies_id,movie_id,indent=4)
	movie_id.close()

###########################    Task 13   ##############################

path="./moviedetailcast.json"
if os.path.exists(path):
	file=json.load(open("moviedetailcast.json","r"))
	pprint(file)


else:

	file=json.load(open("imdb.json","r"))
	moviedetail=[]
	for i in file:
		ab=random.randint(1,4)
		url=i["url"]
		data=requests.get(url).text
		data=BeautifulSoup(data,"html.parser")
		namedata=data.find("div",class_="title_wrapper")
		a=namedata.find("h1").text
		details_of_movies={}
		index=a.index("(")
		name=""
		for i in range(index):
			name+=a[i]
		name=name.strip()
		details_of_movies["Name"]=name
		runtime=namedata.find("time").text
		details_of_movies["Time"]=(runtime.strip())
		genre=[]
		genres=namedata.find_all("a")
		for i in range(1,len(genres)-1):
			genre.append(genres[i].text)
		details_of_movies["Genre"]=(genre)
		biodata=data.find("div",class_="plot_summary")
		bio=biodata.find("div",class_="summary_text").text.strip()
		details_of_movies["Bio"]=(bio)
		directordetail=biodata.find("div",class_="credit_summary_item")
		director=directordetail.find_all("a")
		directors=[]
		for i in director:
			directors.append(i.text)
		details_of_movies["Director"]=(directors)
		countrydetail=data.find("div",id="titleDetails")
		countrydetail=countrydetail.find_all("div",class_="txt-block")
		if (countrydetail[0].find("h4").text)=="Country:":
			country=countrydetail[0].find("a").text
		else:
			country=countrydetail[1].find("a").text
		details_of_movies["Country"]=(country)
		if (countrydetail[1].find("h4").text)=="Language:":
			languages=countrydetail[1].find_all("a")
		else:
			languages=countrydetail[2].find_all("a")
		language=[]
		for i in languages:
			language.append(i.text)
		details_of_movies["Language"]=(language)
		postertag=data.find("div",class_="poster")
		poster=postertag.find("img")["src"]
		details_of_movies["Poster"]=(poster)
		file=url+"fullcredits?ref_=tt_cl_sm#cast"
		datas=requests.get(file).text
		soup=BeautifulSoup(datas,"html.parser")
		castdata=soup.find("table",class_="cast_list")
		cast=castdata.find_all("td",class_=False)
		id_data=[]
		for i in cast:
			cast={}
			ids=i.find("a")["href"]
			ids=ids.split("/")
			ids=ids[2]
			names=(i.text).strip()
			cast["id"]=ids
			cast["Names"]=names
			id_data.append(cast)
		details_of_movies["Cast"]=id_data
		moviedetail.append(details_of_movies)
		time.sleep(ab)
	file=open("moviedetailcast.json","w")
	filedata=json.dump(moviedetail,file,indent=4)
	file.close()


###########################    Task 14   ##############################


path="./task14.json"
if os.path.exists(path):
	files=json.load(open("task14.json","r"))
	print(files)

else:
	movies=json.load(open("moviedetailcast.json","r"))
	Maindict={}
	for i in movies:
		cast=i["Cast"]
		for j in range(len(i)-1):
			mainactor=cast[j]
			mainactorid=mainactor["id"]
			main_actor_name=mainactor["Names"]
			second_dict={}
			second_dict["Name"]=main_actor_name
			frequent_co_actors=[]	
			count=0
			actors=cast[j+1]
			actors_name=actors["Names"]
			dict_of_actors={}	
			V=actors["id"]
			dict_of_actors["id"]=V
			dict_of_actors["Name"]=actors_name
			for k in movies:
				k=k["Cast"]
				movie_actor=k[j]
				if main_actor_name==movie_actor["Names"]:
					for l in k:
						if actors_name==l["Names"]:
							count+=1
			dict_of_actors["num_movies"]=count
			frequent_co_actors.append(dict_of_actors)
			second_dict["frequent_co_actors"]=frequent_co_actors
			Maindict[mainactorid]=second_dict

	data=open("task14.json","w")
	files=json.dump(Maindict,data,indent=4)
	data.close()


###########################    Task 15   ##############################


path="./task15.json"
if os.path.exists(path):
	files=json.load(open("task15.json","r"))
	print(files)

else:
	file=json.load(open("movie_id.json","r"))
	main_dict={}
	for i in file:
		for j in i:
			second_dict={}
			ids=j["id"]
			name=j["Names"]
			second_dict["Names"]=name
			count=0
			for k in file:
				for l in k:
					if j==l:
						count+=1
			second_dict["num_movies"]=count
			main_dict[ids]=second_dict
	data=open("task15.json","w")
	files=json.dump(main_dict,data,indent=4)
	data.close()

#####################################################








