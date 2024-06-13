using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class Envanter : MonoBehaviour
{

    public static int woodCount = 0;
    public static int stoneCount = 0;
    public static int foodCount = 0;
    public static float healthCount = 100;
    public static float hungerCount = 100;
    public static float camphealthCount = 100;
    [SerializeField] private TextMeshProUGUI woodText;
    [SerializeField] private TextMeshProUGUI stoneText;
    [SerializeField] private TextMeshProUGUI foodText;
    [SerializeField] private TextMeshProUGUI healthText;
    [SerializeField] private TextMeshProUGUI hungerText;
    [SerializeField] private TextMeshProUGUI camphealthText;


    public float decreaseRate = 1f;//deðiþkenin ne kadar azalýcaðý
    public float decreaseInterval = 1f;//azalma aralýðý
    public float addHungerInterval = 30f;
    private float timer = 0f;//zamanlýyýcý
    private float addHungerTimer = 0f;

    

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        foodText.text = foodCount.ToString();
        hungerText.text = hungerCount.ToString();
        woodText.text = woodCount.ToString();
        stoneText.text = stoneCount.ToString();
        healthText.text = healthCount.ToString();
        camphealthText.text = camphealthCount.ToString();



        timer += Time.deltaTime / 2;
        addHungerTimer += Time.deltaTime;
        if (timer >= decreaseInterval)
        {
            hungerCount -= decreaseRate;
            camphealthCount -= decreaseRate;
            timer = 0f;

            if (hungerCount <= 0)
            {
                healthCount -= decreaseRate;

            }
            else // Eðer hungerCount 0'dan büyükse healthCount azalmayacak
            {
                healthCount = Mathf.Clamp(healthCount, 0, 100);
                healthCount += decreaseRate;
            }
        }
        // Kontrol noktalarý ekleniyor
        if (hungerCount <= 0)
        {
            hungerCount = 0;
            // Burada örneðin oyun karakterinin ölümü veya baþka bir eylem tetiklenebilir.
        }
        if(hungerCount >= 100)
        {
            hungerCount = 100;
        }

        if (camphealthCount <= 0)
        {
            camphealthCount = 0;
            // Burada örneðin kampýn yok olmasý veya baþka bir eylem tetiklenebilir.
        }

        //if (hungerCount <= 0 && addHungerTimer >= addHungerInterval)
        //{
           // hungerCount += 10;
           // addHungerTimer = 0f;
        //}
        //if (healthCount <= 0 || camphealthCount <= 0)
        //{
            // Tüm envanter öðelerini varsayýlan deðerlere sýfýrla
           // ResetInventory();
            
        //}

    }
    public static void ResetInventory()
    {
        woodCount = 0;
        stoneCount = 0;
        foodCount = 0;
        healthCount = 100;
        hungerCount = 100;
        camphealthCount = 100;
        Timer.day = 0;
        Timer.hour = 0;

        // Karakteri baþlangýç noktasýna yerleþtir
       // transform.position = spawnPoint;
    }
}
