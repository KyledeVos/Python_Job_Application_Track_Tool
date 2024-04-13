# Regex needed for search of applications
import re

class DbReader():

    def __init__(self):
        pass
    
    # ----------------------------------------------------------------------------------
    # Generic Functions

    def retrieve_all_data(self, cursor, table_name):
        return cursor.execute(f"SELECT * FROM {table_name}").fetchall()
    
    def retrieve_single_col_list(self, cursor, column, table_name):
        return [item[0] for item in cursor.execute(f"SELECT {column} FROM {table_name}").fetchall()]
    
    def retrieve_single_col(self, cursor, id, column_name, table_name):
        return cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE id={id}").fetchone()

    def retrieve_id_single_col(self, cursor, column, table_name):
         return cursor.execute(f"SELECT id, {column} FROM {table_name}").fetchall()
       
    def retrieve_single_row(self, cursor, id, table_name):
        return cursor.execute(f"SELECT * FROM {table_name} WHERE id={id}").fetchone()
        
    def retrieve_col_specific(self, cursor, columns, table_name):
        return cursor.execute(f"SELECT id, {', '.join(columns)} FROM {table_name}").fetchall()
    
    def retrieve_column_names(self, cursor, table_name):
        cursor.execute(f"SELECT * FROM {table_name}")
        return [name[0] for name in cursor.description]
    
    def retrieve_single_row_and_col_names(self, cursor, id, table_name):
        columns = self.retrieve_column_names(cursor, table_name)
        data = self.retrieve_single_row(cursor, id, table_name)

        return list(zip(columns, data))

    
    # ----------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------
    # Data Specific Functions

    def retrieve_job_application_date_ordered(self, cursor, columns, table_name, date_order):
        if date_order == "recent":
            return cursor.execute(f"SELECT id, {', '.join(columns)} FROM {table_name} ORDER BY date DESC").fetchall()
        elif date_order == "oldest":
            return cursor.execute(f"SELECT id, {', '.join(columns)} FROM {table_name} ORDER BY date ASC").fetchall()
        

     # ----------------------------------------------------------------------------------
    def retrieve_search_job_applications_date_ordered(self, cursor, table_name, title_cols, search_cols, search_text, date_order):
        # retrieve all job application data
        if date_order == "recent":
            all_data = cursor.execute(f"SELECT id, {', '.join(search_cols)} FROM {table_name}").fetchall()
        elif date_order == "oldest":
            all_data = cursor.execute(f"SELECT id, {', '.join(search_cols)} FROM {table_name}").fetchall()

        # list to store application id's with desired field data matching (or partially matching) search text
        match_id_list = []

        # check each application
        for job_tup in all_data:
            # hold id of current application
            id = job_tup[0]
            # check each field value
            for val in job_tup[1:]:
                # confirm field has data
                if val.strip()!= "":
                    # remove case limitations and any whitespace when performing search
                    if val.strip().lower().replace(" ", "").find(search_text.lower().strip().replace(" ", "") ) != -1:
                        match_id_list.append(id)

        if len(match_id_list) == 0:
            # return none for no matches
            return None
        
        else:
            # list to store matching applications
            matched_applications = []

            for id in match_id_list:
                query = f"SELECT id, {', '.join(title_cols)} FROM {table_name} WHERE id = {id}"
                matched_applications.append(cursor.execute(query).fetchone())

            return matched_applications

        


     # ----------------------------------------------------------------------------------
    def retrieve_configured_job_data(self, cursor, table_name, single_data, large_box_data, fk_data, id=None):
        
        combined_data = {}
        menu_data = []
        
        # retrieve all column names and raw data incl. id's of linked tables
        column_names = [name for name in self.retrieve_column_names(cursor, table_name)]
        if id != None:
            raw_data = list(self.retrieve_single_row_and_col_names(cursor, id, table_name))

            # existing data present, combine existing column names with saved respective data
            single_data_config = []
            large_data_config = []

            for data_col_tup in raw_data:
                # ---- SINGLE DATA CONFIGURATION
                if data_col_tup[0] in single_data:
                    single_data_config.append(data_col_tup)

                # ---- LARGE BOX DATA CONFIGURATION
                elif data_col_tup[0] in large_box_data:
                    large_data_config.append(data_col_tup)

                # ---- FK DATA (menu options with data held in foreign table)
                elif data_col_tup[0] in fk_data['job_application_cols']:
                    table_name_index = fk_data['job_application_cols'].index(data_col_tup[0])
                    fk_table_name = fk_data['fk_table_data'][table_name_index][0]

                    # retrieve current set value
                    set_value = self.retrieve_single_row(cursor, data_col_tup[1], fk_table_name)[1]
                    # retrieve all possible values
                    current_data = [val for val in self.retrieve_all_data(cursor, fk_table_name)]
                    menu_data.append((fk_table_name.title().replace("_", " "), current_data, set_value))
                    
            combined_data['single_data'] = single_data_config
            combined_data['large_box_data'] = large_data_config
            combined_data['menu_data'] = menu_data

        else:
            # NO existing data (new application) - just add column names
            combined_data['single_data'] = single_data
            combined_data['large_box_data'] = large_box_data

            for data_tup in fk_data['fk_table_data']:
                fk_table_name = data_tup[0]
                current_data = [val for val in self.retrieve_all_data(cursor, fk_table_name)]
                menu_data.append((fk_table_name.title().replace("_", " "), current_data))

            combined_data['menu_data'] = menu_data

        return combined_data
        

    def retrieve_fk_data_columns(self, cursor, fk_tables = None):

        # list to hold each foreign key data for job instance ComboBoxes
        fk_data = []

        # retrieve foreign table data
        if fk_tables is not None:
            for fk_tup in fk_tables['fk_table_data']:
                    #fk_tup[0] = table name , fk_tup[1] = desired column name
                    data_list = list(cursor.execute(f"SELECT id, {fk_tup[1]} FROM {fk_tup[0]}").fetchall())
                    fk_data.append([fk_tup[1].title().replace("_", " "), data_list])

        return fk_data
    
    
    # Helper Function to remove desired columns and matching value using index
    def remove_col_and_val(self, col_data, val_data, remove_cols, return_One = False):

        try:
            for col in remove_cols:
                col_index = col_data.index(col)
                col_data.pop(col_index)
                if return_One == True:
                    val_data.pop(col_index)
                else:
                    for result_row in val_data:
                        result_row.pop(col_index)
        except ValueError:
            print(f"ERROR: Colummn '{col}'' is not present for job progress column removal in db_reader")
            
        return {
            'col_list': col_data,
            'val_list': val_data
        }


    def retrieve_progress_rows_complex(self, cursor, table_name, identification_column, identification_value,
                              fk_tables, large_box_cols, remove_cols, return_one, display_only, 
                              order_by_col = None, order = None):
        
        # retrieve column names
        column_names = self.retrieve_column_names(cursor,  table_name)

        # Build Query and data tup:
        query = f"SELECT * FROM {table_name} WHERE {identification_column} = ?"
        data_list = [identification_value]

        # Check for data order specification
        if order_by_col != None:
            query += f" ORDER BY {order_by_col}"

        # determine order 
        if order != None:
            if order == "recent":
                query += " DESC"
            elif order == "oldest":
                query += " ASC"

        if return_one:
            query += " LIMIT 1"

        if return_one == False:
            retrieved_data = cursor.execute(query, tuple(data_list)).fetchall()
            if retrieved_data != None:
                # convert each returned job progress instance to tuple stored in raw_data list
                raw_data = [list(tup) for tup in retrieved_data]
            else:
                # No existing job progress data
                return None
            
        else:
            raw_data = cursor.execute(query, tuple(data_list)).fetchone()
            if raw_data != None:
                raw_data = list(raw_data)
            else:
                # No existing job progress data
                return None

        # remove any desired columns and data from lists
        remaining_data = self.remove_col_and_val(column_names, raw_data, remove_cols, return_one)

        # configure remaining columns for foreign table data
        for count, fk_tup in enumerate(fk_tables['fk_table_data']):
            # retrieve index position of current column that contains menu (Option Menu) id
            col_index = remaining_data['col_list'].index(fk_tables['progress_table_cols'][count])

            # 1) Display Data Only - Option Menu Data Held by Foreign Key Tables does not require Tkinter OptionMenu
            # retrieve index position for foreign key data
            # Build Query:
            # fk_tup[0] = table_name, fk_tup[1] = associated column name
            query = f"SELECT {fk_tup[1]} FROM {fk_tup[0]} WHERE id = ?"

            if return_one == True:
                # change data value in val_list from id to value stored in fk table
                set_value = cursor.execute(query, (remaining_data['val_list'][col_index],)).fetchone()[0]

                if display_only == True:
                    remaining_data['val_list'][col_index] = set_value
                else:
                    query = f"SELECT id, {fk_tup[1]} FROM {fk_tup[0]}"
                    remaining_data['val_list'][col_index] = (set_value, cursor.execute(query).fetchall())
            else:
                # loop through each job process data set and change data value from id to corresponding value in fk_table
                for values_list in remaining_data['val_list']:
                    set_value = cursor.execute(query, (values_list[col_index],)).fetchone()[0]
                    if display_only == True:
                        values_list[col_index] = set_value
                    else:
                        second_query = f"SELECT id, {fk_tup[1]} FROM {fk_tup[0]}"
                        values_list[col_index] = (set_value, cursor.execute(second_query).fetchall())

            # change name of column in col_list
            remaining_data['col_list'][col_index] = fk_tup[1]

            # add column names of large box data and foreign-table data
            # needed by calling function to determine tkinter element for display
            remaining_data['column_info'] = [('large_box_columns', large_box_cols)]

            # Retrieve foreign_key tables joining column name
            fk_cols = []
            for fk_tup in fk_tables['fk_table_data']:
                fk_cols.append(fk_tup[1])
            
            remaining_data['column_info'].append(('fk_columns', fk_cols))

        return remaining_data
    

    def retrieve_job_notes_data(self, cursor, table_name, search_column, search_val, 
                                order_col = None, order = None):
        if order is None:
            query = f"SELECT * FROM {table_name} WHERE {search_column} = {search_val} ORDER BY {order_col} DESC"
        else:
            query = f"SELECT * FROM {table_name} WHERE {search_column} = {search_val} ORDER BY {order_col} {order}"
        
        return cursor.execute(query).fetchall()


    def check_incomplete_notes(self, cursor, table_name, status_field, search_field, search_val):
        status_vals =  cursor.execute(f"SELECT {status_field} from {table_name} where {search_field} == {search_val}").fetchall()
        
        for val_tup in status_vals:
            if 0 in val_tup:
                return True
            
        return False
    

    def check_note_data(self, cursor, table_name, search_field, search_val):
                if cursor.execute(f"SELECT * from {table_name} where {search_field} == {search_val}").fetchone() is None:
                    return False
                else:
                    return True










       

