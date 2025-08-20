using System.Data;
using System.Reflection;
using TrialBalanceApi.Data;

namespace TrialBalanceApi.Repositories
{
    public class BaseRepository : IBaseRepository
    {
        protected readonly IDbConnectionFactory _connectionFactory;

        public BaseRepository(IDbConnectionFactory connectionFactory)
        {
            _connectionFactory = connectionFactory;
        }

        public async Task<T?> QuerySingleOrDefaultAsync<T>(string sql, object? parameters = null)
        {
            return await Task.Run(() =>
            {
                using var connection = _connectionFactory.CreateConnection();
                using var command = CreateCommand(sql, parameters, connection);
                
                connection.Open();
                using var reader = command.ExecuteReader();
                
                if (reader.Read())
                {
                    return MapToObject<T>(reader);
                }
                
                return default(T);
            });
        }

        public async Task<IEnumerable<T>> QueryAsync<T>(string sql, object? parameters = null)
        {
            return await Task.Run(() =>
            {
                using var connection = _connectionFactory.CreateConnection();
                using var command = CreateCommand(sql, parameters, connection);
                
                connection.Open();
                using var reader = command.ExecuteReader();
                
                var results = new List<T>();
                while (reader.Read())
                {
                    results.Add(MapToObject<T>(reader));
                }
                
                return results;
            });
        }

        public async Task<int> ExecuteAsync(string sql, object? parameters = null)
        {
            return await Task.Run(() =>
            {
                using var connection = _connectionFactory.CreateConnection();
                using var command = CreateCommand(sql, parameters, connection);
                
                connection.Open();
                return command.ExecuteNonQuery();
            });
        }

        private static IDbCommand CreateCommand(string sql, object? parameters, IDbConnection connection)
        {
            var command = connection.CreateCommand();
            command.CommandText = sql;
            
            if (parameters != null)
            {
                AddParameters(command, parameters);
            }
            
            return command;
        }

        private static void AddParameters(IDbCommand command, object parameters)
        {
            var properties = parameters.GetType().GetProperties(BindingFlags.Public | BindingFlags.Instance);
            
            foreach (var property in properties)
            {
                var parameter = command.CreateParameter();
                parameter.ParameterName = $"@{property.Name}";
                parameter.Value = property.GetValue(parameters) ?? DBNull.Value;
                command.Parameters.Add(parameter);
            }
        }

        private static T MapToObject<T>(IDataReader reader)
        {
            if (typeof(T) == typeof(string))
            {
                return (T)(object)reader.GetString(0);
            }
            
            if (typeof(T) == typeof(int))
            {
                return (T)(object)reader.GetInt32(0);
            }
            
            if (typeof(T) == typeof(decimal))
            {
                return (T)(object)reader.GetDecimal(0);
            }
            
            if (typeof(T) == typeof(DateTime))
            {
                return (T)(object)reader.GetDateTime(0);
            }
            
            if (typeof(T) == typeof(bool))
            {
                return (T)(object)reader.GetBoolean(0);
            }

            // Handle dynamic objects
            if (typeof(T) == typeof(object) || typeof(T).Name == "Object")
            {
                var expando = new System.Dynamic.ExpandoObject() as IDictionary<string, object>;
                for (int i = 0; i < reader.FieldCount; i++)
                {
                    expando[reader.GetName(i)] = reader.IsDBNull(i) ? null : reader.GetValue(i);
                }
                return (T)(object)expando;
            }

            // Handle complex objects using reflection
            var instance = Activator.CreateInstance<T>();
            var properties = typeof(T).GetProperties(BindingFlags.Public | BindingFlags.Instance);
            
            foreach (var property in properties)
            {
                if (property.CanWrite)
                {
                    try
                    {
                        var ordinal = reader.GetOrdinal(property.Name);
                        if (!reader.IsDBNull(ordinal))
                        {
                            var value = reader.GetValue(ordinal);
                            if (value != null && value != DBNull.Value)
                            {
                                // Handle type conversion
                                if (property.PropertyType != value.GetType())
                                {
                                    value = Convert.ChangeType(value, property.PropertyType);
                                }
                                property.SetValue(instance, value);
                            }
                        }
                    }
                    catch (IndexOutOfRangeException)
                    {
                        // Column doesn't exist, skip
                    }
                }
            }
            
            return instance;
        }
    }
}
