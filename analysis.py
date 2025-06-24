import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset
df = pd.read_csv("C:/Users/Swara/Desktop/Git_projects/data-job-salaries-2025/data/DataScience_Salaries.csv")

# Display basic info
print("🔍 Dataset Preview:\n", df.head())
print("\n📊 Summary Stats:\n", df.describe())

# Salary by Job Category and Experience
plt.figure(figsize=(10,6))
sns.boxplot(data=df, x='experience_level', y='salary_in_usd', hue='job_category')
plt.title("Salary (USD) by Experience and Job Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("salary_by_category.png")
plt.show()

# Average salary by work setting
avg_salary = df.groupby("work_setting")["salary_in_usd"].mean()
print("\n💼 Avg Salary by Work Setting:\n", avg_salary)

# Plot salary by work setting
avg_salary.plot(kind="bar", title="Average Salary by Work Setting")
plt.ylabel("Salary in USD")
plt.tight_layout()
plt.savefig("avg_salary_by_setting.png")
plt.show()

# Salary by employee residence
top_countries = df['employee_residence'].value_counts().head(5).index
filtered = df[df['employee_residence'].isin(top_countries)]

fig = px.box(filtered, x="employee_residence", y="salary_in_usd", color="experience_level",
             title="Salaries by Country & Experience")
fig.write_html("salary_by_country.html")
fig.show()
