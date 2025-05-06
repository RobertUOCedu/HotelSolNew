using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace HotelSOL.Client
{
    public static class ScriptRunner
    {
        public static void EjecutarScriptPython(string relativeScriptPath)
        {
            try
            {
                // Sube 5 niveles desde /bin/Debug/netX/ hasta la raíz de la solución
                string baseDir = AppDomain.CurrentDomain.BaseDirectory;
                string solutionRoot = Directory.GetParent(baseDir)!.Parent!.Parent!.Parent!.Parent!.FullName;

                // Ruta al script dentro de HotelSOL/ConexionOdoo/...
                string scriptFullPath = Path.Combine(solutionRoot, "HotelSOL", "ConexionOdoo", relativeScriptPath);

                var psi = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"\"{scriptFullPath}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using (var process = Process.Start(psi))
                {
                    string output = process.StandardOutput.ReadToEnd();
                    string error = process.StandardError.ReadToEnd();
                    process.WaitForExit();

                    if (!string.IsNullOrWhiteSpace(error))
                    {
                        MessageBox.Show($"ERROR al ejecutar {relativeScriptPath}:\n\n{error}", "Error en script", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                    else
                    {
                        MessageBox.Show($"Script '{relativeScriptPath}' ejecutado correctamente:\n\n{output}", "Éxito", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                }
            }
            catch (System.Exception ex)
            {
                MessageBox.Show($"Excepción al ejecutar {relativeScriptPath}:\n{ex.Message}", "Excepción", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
