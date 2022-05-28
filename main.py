import analysis 
import msr
import pandas as pd

repositorio1 = "app-spring-boot"
url_repositorio1 = "https://github.com/armandossrecife/app-spring-boot.git"
my_path_local = "/Users/armandosoaressousa/git/criticalfiles"

print(f'Clona o repositorio {repositorio1} no path {my_path_local}')
path_to_save_clone = my_path_local + '/' + repositorio1 
analysis.clona_repositorio(url_repositorio1, path_to_save_clone)

# Substitui o . pelo repositorio/
list_of_files_and_directories = analysis.get_list_of_files_and_directories_updated(repositorio1)

# Escolhe o diretorio do source java
# Lista apenas arquivos e diretorios do src/main/java
list_of_files_and_directories_src = analysis.get_list_of_files_and_directories_src(repositorio1)

# Cria um arquivo contendo a quantidade de LOC por arquivo
list_locs_of_files_updated = analysis.get_list_locs_of_files(repositorio1)

# Lista todos os commits de um repositorio
list_commits_promocity = msr.list_all_commits(repositorio1)

# Lista todos os arquivos modificados em cada commit
dict_modified_files_promocity = msr.list_all_modified_files_in_commits(repositorio1)

# Lista todos os commits e seus arquivos modificados
for commit, lista_files in dict_modified_files_promocity.items(): 
  print(commit, [file.filename for file in lista_files])

# 5. Lista a frequência dos arquivos nos commits
dict_frequency_files_commits = msr.get_files_frequency_in_commits(repositorio1)

# 6. Lista a Quantidade de Linhas de Código Modificadas em cada Arquivo
dict_lines_modified_in_files = msr.get_number_of_lines_of_code_changes_in_commits(repositorio1)
dict_java_frequency_commits = analysis.get_dict_java_frequency_commits(dict_frequency_files_commits)
dict_java_lines_modified = analysis.get_dict_java_lines_modified(dict_lines_modified_in_files)

# Converte o dicionário dict_java_frequency_commits em um dataframe
df_java_frequency_commits = analysis.convert_dict_java_frequency_to_dataframe(dict_java_frequency_commits)

# Converte o dicionário dict_java_lines_modified em um dataframe
df_java_lines_modified = analysis.convert_dict_java_lines_modified_to_dataframe(dict_java_lines_modified)

# Faz o merge das informações para criar um dataframe contendo o arquivo, a frequência de Commits e Linhas Modificadas de cada arquivo ao longo do tempo
df_fc_ml = analysis.merge_dataframes_java_frequency(df_java_frequency_commits, df_java_lines_modified)
df_fc_ml

print(f'{df_fc_ml}')

analysis.generate_sccater_plot(df_fc_ml, repositorio1)
# generate_sccater_plot_2(df_fc_ml, repositorio1)

df_boxplot_fc = analysis.generate_box_plot_frequency(df_fc_ml)

fc_q1, fc_q2, fc_q3, fc_q4 = analysis.get_quartiles_frequency(df_boxplot_fc)
print(f'Quartis da Frequencia de Commits Q1: {fc_q1}, Q2: {fc_q2}, Q3: {fc_q3}, Q4: {fc_q4}')

df_boxplot_lm = analysis.generate_box_plot_lines_modified(df_fc_ml)

lm_q1, lm_q2, lm_q3, lm_q4 = analysis.get_quartiles_lines_modified(df_boxplot_lm)
print(f'Quartis da Linhas Modificadas Q1: {lm_q1}, Q2: {lm_q2}, Q3: {lm_q3}, Q4: {lm_q4}')

# Lista os arquivos com maior frequência de commits e mais linhas modificadas ao longo do tempo
my_query = f"Frequency >= {fc_q3[0]} and lines_modified >= {lm_q3[0]}"
print(my_query)
df_arquivos_criticos = df_fc_ml.query(my_query)
qtd_arquivos_criticos = df_arquivos_criticos.shape[0]
qtd_arquivos_java = df_fc_ml.shape[0]
print(f'Qtd arquivos críticos: {qtd_arquivos_criticos}, Total de Arquivos .java {qtd_arquivos_java}')
print(f'{round(qtd_arquivos_criticos/qtd_arquivos_java, 2)*100}% dos arquivos .java são críticos')

total_linhas_modificadas = sum(df_fc_ml['lines_modified'])
linhas_modificadas_arquivos_criticos = sum(df_arquivos_criticos['lines_modified'])
print(f'Qtd de linhas modificadas pelos arquivos críticos: {linhas_modificadas_arquivos_criticos}, Total de linhas de código alteradas ao longo do tempo: {total_linhas_modificadas}')
print(f'{round(linhas_modificadas_arquivos_criticos/total_linhas_modificadas, 2)*100}% do esforço de modificação é com arquivos críticos')

qaj = [qtd_arquivos_java]
laaj = [total_linhas_modificadas]
qac = [qtd_arquivos_criticos]
pac = [round(qtd_arquivos_criticos/qtd_arquivos_java,2)*100]
laac = [linhas_modificadas_arquivos_criticos]
plaac = [round(linhas_modificadas_arquivos_criticos/total_linhas_modificadas, 2)*100]

dict_ = {'Repository': [repositorio1], 'qaj': qaj, 'qac': qac, 'laaj': laaj, 'laac': laac, 'pac': pac, 'plaac': plaac}
df_from_dict = pd.DataFrame.from_dict(dict_)
print(f'{df_from_dict}')