import pandas as pd

df = pd.read_csv("logs.csv",encoding_errors="ignore")


# adding gen ed info:
dfs2 = pd.read_csv("courses.csv",encoding_errors="ignore")
df = pd.merge(df, dfs2[["Course", "CS"]], on="Course")

df.fillna("", inplace=True)

# get rid of courses that have multiple sections
df.drop_duplicates(subset="Course",inplace=True)

# get rid of discussions
df = df[df["Meeting Type (Discussion Lecture etc)"] != "DIS"]

# get 2pm courses
df = df[df["Start Time"] == "02:00 PM"].reset_index(drop=True)

# get courses where the meeting days are either M W or F
days_of_the_week = ["M","W","F"]
df = df[df['Meeting Days'].str.contains('|'.join(days_of_the_week))]
print(df)

df.to_csv("2pmcourses.csv", index=False)