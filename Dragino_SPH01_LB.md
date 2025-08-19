```lua
#!/usr/bin/lua
local json = require('json') -- Assicurati di avere un modulo JSON disponibile, ad esempio 'dkjson' o 'cjson'
print("START")

-- Funzione helper per aggiungere uno zero iniziale ai numeri inferiori a 10
local function getzf(c_num)
    if c_num < 10 then
        return '0' .. tostring(c_num)
    else
        return tostring(c_num)
    end
end

-- Funzione helper per formattare una data da un timestamp
local function getMyDate(str)
    print("START GET DATE")
    local c_Date
    local timestamp = tonumber(str)

    if timestamp > 9999999999 then
        c_Date = os.date("*t", math.floor(timestamp / 1000)) -- Converti ms in secondi
    else
        c_Date = os.date("*t", timestamp)
    end

    local c_Year = c_Date.year
    local c_Month = c_Date.month
    local c_Day = c_Date.day
    local c_Hour = c_Date.hour
    local c_Min = c_Date.min
    local c_Sen = c_Date.sec

    local c_Time = c_Year .. '-' .. getzf(c_Month) .. '-' .. getzf(c_Day) .. ' ' .. getzf(c_Hour) .. ':' .. getzf(c_Min) .. ':' .. getzf(c_Sen)
    return c_Time
end

-- Funzione per la decodifica dei dati di log (fPort 0x03)
local function datalog(i, bytes)
    print("START DATALOG")
    local aa = (bit.bor(bit.lshift(bytes[i + 1], 8), bytes[i + 2])) / 10 -- bytes sono 1-based in Lua
    local bb = (bit.bor(bit.lshift(bytes[i + 3], 8), bytes[i + 4])) / 10
    local cc = (bit.bor(bit.lshift(bytes[i + 5], 8), bytes[i + 6])) / 10
    local dd = bytes[i + 7]
    local ee = getMyDate(tostring(bit.bor(bit.lshift(bytes[i + 8], 24), bit.lshift(bytes[i + 9], 16), bit.lshift(bytes[i + 10], 8), bytes[i + 11])))

    -- Si noti che la stringa JSON risultante per datalog non è un JSON valido se concatenata direttamente
    -- Il codice JS originale restituisce una stringa non valida per un JSON, quindi la mantengo simile
    -- per coerenza, ma per un JSON valido dovresti costruire una tabella e poi codificarla.
    local str = string.format('[PH:%.1f,Temperature:%.1f,DS18B20_Temperature:%.1f,s_flag:%d,time:%s],', aa, bb, cc, dd, ee)
    return str
end

-- Funzione principale di decodifica
function Decode(fPort, bytes)
    print("START DECODE")
    -- Assicurati che 'bytes' sia una tabella di numeri e sia 1-based per coerenza con l'uso di 'bytes[i+x]'
    -- Se l'input 'bytes' è 0-based, dovrai aggiustare gli indici (+1 a tutti gli accessi).
    -- Per questo esempio, assumo che 'bytes' sia già 1-based o che tu lo converta prima di chiamare Decode.

    if fPort == 0x02 then
        local value = bit.band(bit.bor(bit.lshift(bytes[1], 8), bytes[2]), 0x3FFF)
        local batV = value / 1000 -- Battery, units:V

        value = bit.bor(bit.lshift(bytes[3], 8), bytes[4])
        if bit.band(bytes[3], 0x80) ~= 0 then
            value = bit.bor(value, 0xFFFF0000)
        end
        local temp_DS18B20 = value / 10 -- DS18B20, temperature

        value = bit.bor(bit.lshift(bytes[5], 8), bytes[6])
        local PH1 = value / 100

        value = bit.bor(bit.lshift(bytes[7], 8), bytes[8])
        local temp = 0
        if bit.rshift(bit.band(value, 0x8000), 15) == 0 then
            temp = value / 10 -- temp_SOIL, temperature
        elseif bit.rshift(bit.band(value, 0x8000), 15) == 1 then
            temp = (value - 0xFFFF) / 10
        end

        local i_flag = bytes[9]
        local mes_type = bytes[11]

        if #bytes == 11 then
            return {
                Node_type = "SPH01-LB",
                Bat = batV,
                TempC_DS18B20 = temp_DS18B20,
                PH1_SOIL = PH1,
                TEMP_SOIL = temp,
                Interrupt_flag = i_flag,
                Message_type = mes_type
            }
        end
    elseif fPort == 0x03 then
        local data_sum = ""
        for i = 0, #bytes - 1, 11 do -- Iterazione basata su 0 per la logica di 'i' nel JS
            local data = datalog(i, bytes)
            if i == 0 then
                data_sum = data
            else
                data_sum = data_sum .. data
            end
        end
        return {
            Node_type = "SPH01-LB",
            DATALOG = data_sum
        }
    elseif fPort == 0x05 then
        local sub_band
        local freq_band
        local sensor

        if bytes[1] == 0x2C then
            sensor = "SPH01-LB"
        end

        if bytes[5] == 0xff then
            sub_band = "NULL"
        else
            sub_band = bytes[5]
        end

        if bytes[4] == 0x01 then
            freq_band = "EU868"
        elseif bytes[4] == 0x02 then
            freq_band = "US915"
        elseif bytes[4] == 0x03 then
            freq_band = "IN865"
        elseif bytes[4] == 0x04 then
            freq_band = "AU915"
        elseif bytes[4] == 0x05 then
            freq_band = "KZ865"
        elseif bytes[4] == 0x06 then
            freq_band = "RU864"
        elseif bytes[4] == 0x07 then
            freq_band = "AS923"
        elseif bytes[4] == 0x08 then
            freq_band = "AS923_1"
        elseif bytes[4] == 0x09 then
            freq_band = "AS923_2"
        elseif bytes[4] == 0x0A then
            freq_band = "AS923_3"
        elseif bytes[4] == 0x0B then
            freq_band = "CN470"
        elseif bytes[4] == 0x0C then
            freq_band = "EU433"
        elseif bytes[4] == 0x0D then
            freq_band = "KR920"
        elseif bytes[4] == 0x0E then
            freq_band = "MA869"
        end

        local firm_ver = tostring(bit.band(bytes[2], 0x0f)) .. '.' .. tostring(bit.rshift(bit.band(bytes[3], 0xf0), 4)) .. '.' .. tostring(bit.band(bytes[3], 0x0f))
        local bat = (bit.bor(bit.lshift(bytes[6], 8), bytes[7])) / 1000

        return {
            SENSOR_MODEL = sensor,
            FIRMWARE_VERSION = firm_ver,
            FREQUENCY_BAND = freq_band,
            SUB_BAND = sub_band,
            BAT = bat
        }
    end
    return nil -- Nessuna decodifica corrispondente
end

-- Funzione principale per simulare l'ambiente di decodifica
-- Input: una tabella con 'fPort' e 'bytes'
-- Ad esempio: decodeUplink({fPort = 2, bytes = {0x0F, 0xAB, 0x01, 0x2C, ...}})
function decodeUplink(input)
    -- Converti i byte da 0-based a 1-based se necessario, a seconda di come li ricevi
    -- Qui assumo che 'input.bytes' sia una tabella di numeri (0-255) e verrà trattata come 1-based negli accessi.
    -- Se 'input.bytes' è 0-based, dovresti copiarlo in una nuova tabella 1-based.
    local decoded_data = Decode(input.fPort, input.bytes)
    return { data = decoded_data }
end
```