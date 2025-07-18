// Get list of all recaps at build time
const RECAP_FILES = [
    "Above_Gravity_vs_Bodega_Cats_10551_recap.txt",
    "Above_Gravity_vs_Bodega_Cats_10553_recap.txt",
    "Above_Gravity_vs_Bodega_Cats_10676_recap.txt",
    "Above_Gravity_vs_Bodega_Cats_10679_recap.txt",
    "Above_Gravity_vs_Dirty_Birch_10358_recap.txt",
    "Above_Gravity_vs_Do_Not_Disturb_10496_recap.txt",
    "Above_Gravity_vs_Do_Not_Disturb_10640_recap.txt",
    "Above_The_Rim_vs_High_Octane_7511_recap.txt",
    "Above_The_Rim_vs_High_Octane_7514_recap.txt",
    "All_Honest_Reps_vs_High_Octane_7501_recap.txt",
    "All_Honest_Reps_vs_High_Octane_7504_recap.txt",
    "Ball_in_Peace_vs_Before_The_Fame_6562_recap.txt",
    "Before_The_Fame_vs_Ball_in_Peace_6550_recap.txt",
    "Before_The_Fame_vs_Dirty_Birch_7523_recap.txt",
    "Before_The_Fame_vs_GabbaGhouls_6554_recap.txt",
    "Before_The_Fame_vs_Generation_of_Miracles_10249_recap.txt",
    "Before_The_Fame_vs_Lights_Out_6546_recap.txt",
    "Before_The_Fame_vs_Lights_Out_9646_recap.txt",
    "Before_The_Fame_vs_On_Site_6427_recap.txt",
    "Before_The_Fame_vs_On_Site_8287_recap.txt",
    "Bodega_Cats_vs_All_Honest_Reps_7482_recap.txt",
    "Bodega_Cats_vs_Before_The_Fame_9389_recap.txt",
    "Bodega_Cats_vs_Generation_of_Miracles_9657_recap.txt",
    "Bodega_Cats_vs_Generation_of_Miracles_9665_recap.txt",
    "Bodega_Cats_vs_High_Octane_10646_recap.txt",
    "Bodega_Cats_vs_Lights_Out_7525_recap.txt",
    "Bodega_Cats_vs_Liquid_Pro_Am_8312_recap.txt",
    "Bodega_Cats_vs_Liquid_Underground_7455_recap.txt",
    "Bodega_Cats_vs_Liquid_Underground_7485_recap.txt",
    "Bodega_Cats_vs_New_Era_8293_recap.txt",
    "Bodega_Cats_vs_NoPlaysOff_9675_recap.txt",
    "Bodega_Cats_vs_On_Site_9396_recap.txt",
    "Bodega_Cats_vs_State_Mafia_10465_recap.txt",
    "Bodega_Cats_vs_Sup_6642_recap.txt",
    "Bodega_Cats_vs_UP_THE_SCORE_10518_recap.txt",
    "Bodega_Cats_vs_UP_THE_SCORE_10521_recap.txt",
    "Bodega_Cats_vs_Watch_Greatness_7580_recap.txt",
    "Capital_City_Cats_vs_Bodega_Cats_10487_recap.txt",
    "Capital_City_Cats_vs_Lights_Out_10483_recap.txt",
    "Capitol_City_Cats_vs_RWG_10274_recap.txt",
    "Capitol_City_Cats_vs_RWG_10287_recap.txt",
    "Coatesville_UPA_vs_Lights_Out_7472_recap.txt",
    "Coatesville_UPA_vs_Lights_Out_7564_recap.txt",
    "Coatesville_UPA_vs_New_Era_8188_recap.txt",
    "Coatesville_UPA_vs_New_Era_8320_recap.txt",
    "Coatesville_UPA_vs_Watch_Greatness_7493_recap.txt",
    "Coatesville_UPA_vs_Watch_Greatness_7499_recap.txt",
    "Dirty_Birch_vs_Above_Gravity_10364_recap.txt",
    "Dirty_Birch_vs_Before_The_Fame_7521_recap.txt",
    "Dirty_Birch_vs_Lights_Out_10471_recap.txt",
    "Dirty_Birch_vs_Lights_Out_10613_recap.txt",
    "Dirty_Birch_vs_Liquid_Underground_10374_recap.txt",
    "Dirty_Birch_vs_On_Site_10616_recap.txt",
    "Dirty_Birch_vs_RuntheClockBoyz_7508_recap.txt",
    "Dirty_Birch_vs_Watch_Greatness_7490_recap.txt",
    "Do_Not_Disturb_vs_Above_Gravity_10493_recap.txt",
    "Do_Not_Disturb_vs_Above_Gravity_10499_recap.txt",
    "Do_Not_Disturb_vs_Dirty_Birch_10670_recap.txt",
    "Do_Not_Disturb_vs_Dirty_Birch_10673_recap.txt",
    "Do_Not_Disturb_vs_Lights_Out_10664_recap.txt",
    "Full_Court_Press_vs_GYG_6628_recap.txt",
    "Full_Court_Press_vs_GYG_6630_recap.txt",
    "Full_Court_Press_vs_Nothing_Less_6473_recap.txt",
    "Full_Court_Press_vs_Nothing_Less_6480_recap.txt",
    "Full_Court_Press_vs_Nothing_Less_6482_recap.txt",
    "GYG_vs_Liquid_Underground_6530_recap.txt",
    "GabbaGhouls_vs_Bodega_Cats_8458_recap.txt",
    "GabbaGhouls_vs_High_Octane_6513_recap.txt",
    "GabbaGhouls_vs_In_Charge_6640_recap.txt",
    "GabbaGhouls_vs_Liquid_Pro_Am_6458_recap.txt",
    "GabbaGhouls_vs_Liquid_Pro_Am_6460_recap.txt",
    "GabbaGhouls_vs_Nothing_Less_6620_recap.txt",
    "GabbaGhouls_vs_Packem_Up_Gaming_6626_recap.txt",
    "GabbaGhouls_vs_Sup_6618_recap.txt",
    "GabbaGhouls_vs_Sup_6624_recap.txt",
    "General_Population_vs_GabbaGhouls_6570_recap.txt",
    "General_Population_vs_GabbaGhouls_6613_recap.txt",
    "General_Population_vs_High_Octane_6505_recap.txt",
    "General_Population_vs_High_Octane_6577_recap.txt",
    "General_Population_vs_In_Charge_6579_recap.txt",
    "General_Population_vs_In_Charge_6636_recap.txt",
    "General_Population_vs_Packem_Up_Gaming_6581_recap.txt",
    "General_Population_vs_Packem_Up_Gaming_6583_recap.txt",
    "General_Population_vs_Sup_6572_recap.txt",
    "General_Population_vs_Team_Solidified_6490_recap.txt",
    "Generation_of_Miracles_vs_Before_The_Fame_10262_recap.txt",
    "Generation_of_Miracles_vs_Bodega_Cats_10548_recap.txt",
    "Generation_of_Miracles_vs_Bodega_Cats_8224_recap.txt",
    "Generation_of_Miracles_vs_High_Octane_10542_recap.txt",
    "Generation_of_Miracles_vs_Lights_Out_10353_recap.txt",
    "Generation_of_Miracles_vs_Lights_Out_10649_recap.txt",
    "Generation_of_Miracles_vs_Lights_Out_6597_recap.txt",
    "Generation_of_Miracles_vs_Lights_Out_6599_recap.txt",
    "Generation_of_Miracles_vs_Lights_Out_7568_recap.txt",
    "Generation_of_Miracles_vs_Liquid_Pro_Am_8296_recap.txt",
    "Generation_of_Miracles_vs_Negative_Zero_10533_recap.txt",
    "Generation_of_Miracles_vs_Nothing_Less_6609_recap.txt",
    "Generation_of_Miracles_vs_On_Site_10637_recap.txt",
    "Generation_of_Miracles_vs_On_Site_7467_recap.txt",
    "Generation_of_Miracles_vs_Team_Solidified_6494_recap.txt",
    "Glue_Guys_vs_Generation_of_Miracles_6611_recap.txt",
    "Glue_Guys_vs_Lights_Out_6585_recap.txt",
    "Glue_Guys_vs_On_Site_8467_recap.txt",
    "Glue_Guys_vs_The_Takeover_8512_recap.txt",
    "GodSpeed_vs_Bodega_Cats_7479_recap.txt",
    "High_Octane_vs_Above_The_Rim_7518_recap.txt",
    "High_Octane_vs_Bodega_Cats_6501_recap.txt",
    "High_Octane_vs_Bodega_Cats_6507_recap.txt",
    "High_Octane_vs_Coatesville_UPA_8179_recap.txt",
    "High_Octane_vs_Coatesville_UPA_8182_recap.txt",
    "High_Octane_vs_Do_Not_Disturb_10505_recap.txt",
    "High_Octane_vs_Do_Not_Disturb_10508_recap.txt",
    "High_Octane_vs_Do_Not_Disturb_10524_recap.txt",
    "High_Octane_vs_Do_Not_Disturb_10527_recap.txt",
    "High_Octane_vs_Do_Not_Disturb_10530_recap.txt",
    "High_Octane_vs_General_Population_6575_recap.txt",
    "High_Octane_vs_Generation_of_Miracles_10545_recap.txt",
    "High_Octane_vs_Lights_Out_10502_recap.txt",
    "High_Octane_vs_Lights_Out_10511_recap.txt",
    "High_Octane_vs_Lights_Out_10514_recap.txt",
    "High_Octane_vs_Liquid_Pro_Am_10581_recap.txt",
    "High_Octane_vs_Liquid_Underground_6534_recap.txt",
    "High_Octane_vs_Nothing_Less_6471_recap.txt",
    "High_Octane_vs_On_Site_10625_recap.txt",
    "High_Octane_vs_Sup_6524_recap.txt",
    "In_Charge_vs_High_Octane_6638_recap.txt",
    "In_Charge_vs_On_Site_6397_recap.txt",
    "Lights_Out_vs_Above_Gravity_10271_recap.txt",
    "Lights_Out_vs_Above_Gravity_10590_recap.txt",
    "Lights_Out_vs_Above_Gravity_10592_recap.txt",
    "Lights_Out_vs_Above_Gravity_9826_recap.txt",
    "Lights_Out_vs_Before_The_Fame_6548_recap.txt",
    "Lights_Out_vs_Before_The_Fame_6587_recap.txt",
    "Lights_Out_vs_Bodega_Cats_10643_recap.txt",
    "Lights_Out_vs_Bodega_Cats_6644_recap.txt",
    "Lights_Out_vs_Bodega_Cats_6646_recap.txt",
    "Lights_Out_vs_Bodega_Cats_7574_recap.txt",
    "Lights_Out_vs_Bodega_Cats_8049_recap.txt",
    "Lights_Out_vs_Capitol_City_Cats_10477_recap.txt",
    "Lights_Out_vs_Capitol_City_Cats_10658_recap.txt",
    "Lights_Out_vs_Coatesville_UPA_7571_recap.txt",
    "Lights_Out_vs_Dirty_Birch_10468_recap.txt",
    "Lights_Out_vs_Dirty_Birch_10474_recap.txt",
    "Lights_Out_vs_Do_Not_Disturb_10661_recap.txt",
    "Lights_Out_vs_Full_Court_Press_6601_recap.txt",
    "Lights_Out_vs_Generation_of_Miracles_6589_recap.txt",
    "Lights_Out_vs_High_Octane_10628_recap.txt",
    "Lights_Out_vs_High_Octane_10631_recap.txt",
    "Lights_Out_vs_Liquid_Pro_Am_6462_recap.txt",
    "Lights_Out_vs_Liquid_Underground_6595_recap.txt",
    "Lights_Out_vs_NO_LOVE_6603_recap.txt",
    "Lights_Out_vs_NO_LOVE_6605_recap.txt",
    "Lights_Out_vs_Negative_Zero_10366_recap.txt",
    "Lights_Out_vs_Negative_Zero_9370_recap.txt",
    "Lights_Out_vs_NoPlaysOff_9548_recap.txt",
    "Lights_Out_vs_NoPlaysOff_9550_recap.txt",
    "Lights_Out_vs_Nothing_Less_6591_recap.txt",
    "Lights_Out_vs_On_Site_10667_recap.txt",
    "Lights_Out_vs_On_Site_6451_recap.txt",
    "Lights_Out_vs_RWG_9410_recap.txt",
    "Liquid_Pro_Am_vs_Bodega_Cats_6303_recap.txt",
    "Liquid_Pro_Am_vs_Bodega_Cats_8309_recap.txt",
    "Liquid_Pro_Am_vs_Generation_of_Miracles_8299_recap.txt",
    "Liquid_Pro_Am_vs_TTO_6454_recap.txt",
    "Liquid_Underground_vs_Above_Gravity_10610_recap.txt",
    "Liquid_Underground_vs_All_Honest_Reps_7964_recap.txt",
    "Liquid_Underground_vs_Dirty_Birch_10583_recap.txt",
    "Liquid_Underground_vs_Dirty_Birch_10585_recap.txt",
    "Liquid_Underground_vs_Dirty_Birch_9366_recap.txt",
    "Liquid_Underground_vs_Fear_Greatness_7577_recap.txt",
    "Liquid_Underground_vs_GYG_6528_recap.txt",
    "Liquid_Underground_vs_High_Octane_6532_recap.txt",
    "Liquid_Underground_vs_Lights_Out_10588_recap.txt",
    "Liquid_Underground_vs_Lights_Out_9358_recap.txt",
    "Liquid_Underground_vs_Negative_Zero_10377_recap.txt",
    "Liquid_Underground_vs_Nothing_Less_6536_recap.txt",
    "Liquid_Underground_vs_Nothing_Less_6540_recap.txt",
    "Liquid_Underground_vs_On_Site_6391_recap.txt",
    "Liquid_Underground_vs_On_Site_6542_recap.txt",
    "NO_LOVE_vs_Liquid_Pro_Am_6456_recap.txt",
    "NO_LOVE_vs_Packem_Up_Gaming_6634_recap.txt",
    "Negative_Zero_vs_Bodega_Cats_9673_recap.txt",
    "Negative_Zero_vs_Lights_Out_9413_recap.txt",
    "Negative_Zero_vs_Liquid_Underground_9304_recap.txt",
    "Negative_Zero_vs_Liquid_Underground_9355_recap.txt",
    "New_Era_vs_All_Honest_Reps_7989_recap.txt",
    "New_Era_vs_Capitol_City_Cats_10490_recap.txt",
    "New_Era_vs_Coatesville_UPA_8185_recap.txt",
    "New_Era_vs_UP_THE_SCORE_9820_recap.txt",
    "New_Era_vs_Vulture_Island_GM_9618_recap.txt",
    "NoPlaysOff_vs_Generation_of_Miracles_10536_recap.txt",
    "NoPlaysOff_vs_Generation_of_Miracles_10539_recap.txt",
    "Nothing_Less_vs_Full_Court_Press_6478_recap.txt",
    "Nothing_Less_vs_High_Octane_6466_recap.txt",
    "Nothing_Less_vs_High_Octane_6503_recap.txt",
    "Nothing_Less_vs_Lights_Out_6593_recap.txt",
    "Nothing_Less_vs_Liquid_Underground_6538_recap.txt",
    "Nothing_Less_vs_On_Site_8473_recap.txt",
    "On_Site_vs_Ball_in_Peace_6558_recap.txt",
    "On_Site_vs_Before_The_Fame_6430_recap.txt",
    "On_Site_vs_Before_The_Fame_8290_recap.txt",
    "On_Site_vs_Bodega_Cats_9386_recap.txt",
    "On_Site_vs_Breakout_Gaming_8487_recap.txt",
    "On_Site_vs_Breakout_Gaming_8490_recap.txt",
    "On_Site_vs_Breakout_Gaming_8495_recap.txt",
    "On_Site_vs_Dirty_Birch_10619_recap.txt",
    "On_Site_vs_Fear_Greatness_7459_recap.txt",
    "On_Site_vs_GYG_8498_recap.txt",
    "On_Site_vs_Gabbaghouls_6436_recap.txt",
    "On_Site_vs_Gabbaghouls_6439_recap.txt",
    "On_Site_vs_Gabbaghouls_6442_recap.txt",
    "On_Site_vs_Generation_of_Miracles_10634_recap.txt",
    "On_Site_vs_Generation_of_Miracles_7462_recap.txt",
    "On_Site_vs_Glue_Guys_8470_recap.txt",
    "On_Site_vs_High_Octane_10622_recap.txt",
    "On_Site_vs_High_Octane_8476_recap.txt",
    "On_Site_vs_In_Charge_6394_recap.txt",
    "On_Site_vs_Lights_Out_10607_recap.txt",
    "On_Site_vs_Lights_Out_10652_recap.txt",
    "On_Site_vs_Lights_Out_10655_recap.txt",
    "On_Site_vs_Lights_Out_6607_recap.txt",
    "On_Site_vs_Lights_Out_7979_recap.txt",
    "On_Site_vs_Lights_Out_8501_recap.txt",
    "On_Site_vs_Liquid_Underground_6388_recap.txt",
    "On_Site_vs_Liquid_Underground_8463_recap.txt",
    "On_Site_vs_Nothing_Less_6400_recap.txt",
    "On_Site_vs_PackemUpGang_6433_recap.txt",
    "On_Site_vs_Team_Solidified_6445_recap.txt",
    "On_Site_vs_The_Takeover_6382_recap.txt",
    "PackemUpGang_vs_Bodega_Cats_9833_recap.txt",
    "PackemUpGang_vs_Bodega_Cats_9844_recap.txt",
    "Packem_Up_Gaming_vs_Ball_in_Peace_6560_recap.txt",
    "Packem_Up_Gaming_vs_Before_The_Fame_6552_recap.txt",
    "Packem_Up_Gaming_vs_Before_The_Fame_6556_recap.txt",
    "Packem_Up_Gaming_vs_High_Octane_6509_recap.txt",
    "Packem_Up_Gaming_vs_High_Octane_6511_recap.txt",
    "Packem_Up_Gaming_vs_NO_LOVE_6632_recap.txt",
    "Packem_Up_Gaming_vs_Nothing_Less_6476_recap.txt",
    "RuntheClockBoyz_vs_Bodega_Cats_7448_recap.txt",
    "RuntheClockBoyz_vs_Bodega_Cats_7451_recap.txt",
    "RuntheClockBoyz_vs_Coatesville_UPA_7470_recap.txt",
    "SWVA_Paradise_vs_Coatesville_UPA_8203_recap.txt",
    "SWVA_Paradise_vs_Coatesville_UPA_8206_recap.txt",
    "Stretch_Belly_Squad_vs_Lights_Out_9822_recap.txt",
    "Stretch_Belly_Squad_vs_Liquid_Underground_9311_recap.txt",
    "Sup_vs_GabbaGhouls_6622_recap.txt",
    "Sup_vs_High_Octane_6518_recap.txt",
    "Sup_vs_High_Octane_6520_recap.txt",
    "Sup_vs_High_Octane_6526_recap.txt",
    "TTO_vs_GabbaGhouls_6566_recap.txt",
    "TTO_vs_GabbaGhouls_6568_recap.txt",
    "TTO_vs_NO_LOVE_6564_recap.txt",
    "Team_Solidified_vs_Generation_of_Miracles_6496_recap.txt",
    "Team_Solidified_vs_Glue_Guys_6484_recap.txt",
    "Team_Solidified_vs_Lights_Out_6488_recap.txt",
    "Team_Solidified_vs_NO_LOVE_6492_recap.txt",
    "Team_Solidified_vs_On_Site_6448_recap.txt",
    "Team_Solidified_vs_On_Site_6486_recap.txt",
    "Team_Solidified_vs_Packem_Up_Gaming_6498_recap.txt",
    "The_Takeover_vs_Glue_Guys_8515_recap.txt",
    "The_Takeover_vs_Glue_Guys_8518_recap.txt",
    "The_Takeover_vs_On_Site_6385_recap.txt",
    "Through_The_Wire_vs_All_Honest_Reps_8200_recap.txt",
    "Through_The_Wire_vs_UMSV_Dolphins_8194_recap.txt",
    "Through_The_Wire_vs_Undecided_8191_recap.txt",
    "UMSV_Dolphins_vs_Through_The_Wire_8197_recap.txt",
    "UP_THE_SCORE_vs_Bodega_Cats_9401_recap.txt",
    "UP_THE_SCORE_vs_New_Era_9818_recap.txt",
    "Undecided_vs_New_Era_7844_recap.txt",
    "Vulture_Island_GM_vs_New_Direction_9616_recap.txt",
    "Watch_Greatness_vs_Coatesville_UPA_7496_recap.txt"
];

// Handle incoming requests
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Handle API endpoint for listing recaps
    if (path === '/api/recaps') {
      return new Response(JSON.stringify(RECAP_FILES), {
        headers: { 
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    // Handle individual recap files
    if (path.startsWith('/recap/')) {
        const fileName = path.split('/').pop();
        if (fileName.endsWith('_recap.txt')) {
            try {
                // Try to fetch the recap file from the recaps directory
                const response = await fetch(new URL(`recaps/${fileName}`, url.origin));
                if (!response.ok) throw new Error('Recap not found');
                
                const text = await response.text();
                
                // Create a simple HTML page to display the recap
                const html = `
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Game Recap: ${fileName.replace('_recap.txt', '')}</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <style>
                            body { 
                                font-family: Arial, sans-serif; 
                                line-height: 1.6; 
                                max-width: 800px; 
                                margin: 0 auto; 
                                padding: 20px;
                            }
                            pre { 
                                white-space: pre-wrap; 
                                background: #f5f5f5; 
                                padding: 15px; 
                                border-radius: 5px;
                                overflow-x: auto;
                            }
                            .back-link { 
                                display: inline-block; 
                                margin-bottom: 20px; 
                                color: #3498db; 
                                text-decoration: none;
                            }
                            .back-link:hover { text-decoration: underline; }
                        </style>
                    </head>
                    <body>
                        <a href="/" class="back-link">← Back to all recaps</a>
                        <h1>${fileName.replace('_recap.txt', '').replace(/_/g, ' ')}</h1>
                        <pre>${text}</pre>
                    </body>
                    </html>
                `;
                
                return new Response(html, {
                    headers: { 'Content-Type': 'text/html' }
                });
            } catch (error) {
                return new Response('Recap not found', { 
                    status: 404,
                    headers: { 'Content-Type': 'text/plain' }
                });
            }
        }
    }

    // For all other requests, serve the static files
    return fetch(request);
  }
};
