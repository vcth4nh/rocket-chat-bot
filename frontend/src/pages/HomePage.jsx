import React, { useState } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Grid,
  Paper,
  IconButton,
  Switch,
  FormControlLabel,
} from "@mui/material";

import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";

const HomePage = () => {
  const [blacklist, setBlacklist] = useState([
    "example",
    "test",
    "thieunang",
    "ngoitrongtoiletgao",
    "momo",
    "suyvl",
    "nhoem",
    "d ae",
    "vctdan",
  ]);
  const [regexList, setRegexList] = useState([
    "^\\d+$",
    "^((25[0-5]|2[0-4][0-9]|[1-9][0-9])(\\.(?!$)|$)){4}$",
  ]);
  const [newWords, setNewWords] = useState("");
  const [newRegex, setNewRegex] = useState("");
  const [editingRegex, setEditingRegex] = useState(null);
  const [editingBlacklist, setEditingBlacklist] = useState(null);
  const [detectSecrets, setDetectSecrets] = useState(false);
  const [wordLimit, setWordLimit] = useState(100);

  const handleBlacklistChange = () => {
    const words = newWords.split(",").map((word) => word.trim());
    setBlacklist([...blacklist, ...words]);
    setNewWords("");
  };

  const handleRegexChange = () => {
    const regexLines = newRegex
      .split("\n")
      .map((regex) => regex.trim())
      .filter(Boolean);
    setRegexList([...regexList, ...regexLines]);
    setNewRegex("");
  };

  const handleEditRegex = (id) => {
    const regexToEdit = regexList[id - 1];
    setEditingRegex({ id, value: regexToEdit });
  };

  const handleEditBlacklist = (id) => {
    const blacklistToEdit = blacklist[id - 1];
    setEditingBlacklist({ id, value: blacklistToEdit });
  };

  const handleSaveEditRegex = () => {
    if (editingRegex) {
      const updatedRegexList = regexList.map((regex, index) =>
        index === editingRegex.id - 1 ? editingRegex.value : regex
      );
      setRegexList(updatedRegexList);
      setEditingRegex(null);
    }
  };

  const handleSaveEditBlacklist = () => {
    if (editingBlacklist) {
      const updatedBlacklistList = blacklist.map((blacklist, index) =>
        index === editingBlacklist.id - 1 ? editingBlacklist.value : blacklist
      );
      setBlacklist(updatedBlacklistList);
      setEditingBlacklist(null);
    }
  };

  const handleSaveToggleAndLimit = () => {
    console.log("Detect Secrets:", detectSecrets);
    console.log("Word Limit:", wordLimit);
  };

  const blacklistColumns = [
    { field: "id", headerName: "Index", width: 100 },
    { field: "word", headerName: "Word", flex: 1 },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <Box>
          <IconButton
            color="primary"
            onClick={() => handleEditBlacklist(params.row.id)}
          >
            <EditIcon />
          </IconButton>
          <IconButton
            color="error"
            onClick={() =>
              setBlacklist(blacklist.filter((_, i) => i !== params.row.id - 1))
            }
          >
            <DeleteIcon />
          </IconButton>
        </Box>
      ),
    },
  ];

  const blacklistRows = blacklist.map((word, index) => ({
    id: index + 1,
    word,
  }));

  const regexColumns = [
    { field: "id", headerName: "Index", width: 100 },
    { field: "regex", headerName: "Regex Pattern", flex: 1 },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <Box>
          <IconButton
            color="primary"
            onClick={() => handleEditRegex(params.row.id)}
          >
            <EditIcon />
          </IconButton>
          <IconButton
            color="error"
            onClick={() =>
              setRegexList(regexList.filter((_, i) => i !== params.row.id - 1))
            }
          >
            <DeleteIcon />
          </IconButton>
        </Box>
      ),
    },
  ];

  const regexRows = regexList.map((regex, index) => ({ id: index + 1, regex }));

  return (
    <Box
      sx={{
        p: 4,
        maxWidth: "1200px",
        margin: "0 auto",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        gap: 4,
      }}
    >
      <Typography variant="h4" color="primary" gutterBottom>
        Configure Policies
      </Typography>

      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Toggle and Word Limit
        </Typography>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={detectSecrets}
                  onChange={(e) => setDetectSecrets(e.target.checked)}
                />
              }
              label="Detect Secrets"
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              variant="outlined"
              label="Word Limit"
              type="number"
              value={wordLimit}
              onChange={(e) => setWordLimit(e.target.value)}
            />
          </Grid>
        </Grid>
        <Box sx={{ mt: 2 }}>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleSaveToggleAndLimit}
          >
            Save Settings
          </Button>
        </Box>
      </Paper>

      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Blacklisted Words
        </Typography>
        {editingBlacklist && (
          <Box sx={{ mb: 2 }}>
            <TextField
              fullWidth
              variant="outlined"
              value={editingBlacklist.value}
              onChange={(e) =>
                setEditingBlacklist({
                  ...editingBlacklist,
                  value: e.target.value,
                })
              }
              placeholder="Thay đổi từ blacklist"
              sx={{ mb: 1 }}
            />
            <Button
              variant="contained"
              color="secondary"
              onClick={handleSaveEditBlacklist}
            >
              Save Edit
            </Button>
          </Box>
        )}
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6}>
            <TextField
              fullWidth
              variant="outlined"
              value={newWords}
              onChange={(e) => setNewWords(e.target.value)}
              placeholder="Enter words to blacklist (comma separated)"
              multiline
              rows={2}
              sx={{ mb: 2 }}
            />
            <Button
              variant="contained"
              color="secondary"
              onClick={handleBlacklistChange}
            >
              Save Changes
            </Button>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle1">
              Current Blacklist ({blacklist.length} words):
            </Typography>
            <Box sx={{ height: 400, mt: 2 }}>
              <DataGrid
                rows={blacklistRows}
                columns={blacklistColumns}
                pageSize={5}
                rowsPerPageOptions={[5]}
                disableSelectionOnClick
                components={{ Toolbar: GridToolbar }}
              />
            </Box>
          </Grid>
        </Grid>
      </Paper>

      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Regex Patterns
        </Typography>
        {editingRegex && (
          <Box sx={{ mb: 2 }}>
            <TextField
              fullWidth
              variant="outlined"
              value={editingRegex.value}
              onChange={(e) =>
                setEditingRegex({ ...editingRegex, value: e.target.value })
              }
              placeholder="Edit regex pattern"
              sx={{ mb: 1 }}
            />
            <Button
              variant="contained"
              color="secondary"
              onClick={handleSaveEditRegex}
            >
              Save Edit
            </Button>
          </Box>
        )}
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6}>
            <TextField
              fullWidth
              variant="outlined"
              value={newRegex}
              onChange={(e) => setNewRegex(e.target.value)}
              placeholder="Enter regex patterns (one per line)"
              multiline
              rows={4}
              sx={{ mb: 2 }}
            />
            <Button
              variant="contained"
              color="secondary"
              onClick={handleRegexChange}
            >
              Save Changes
            </Button>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle1">
              Current Regex Filters ({regexList.length} patterns):
            </Typography>
            <Box sx={{ height: 400, mt: 2 }}>
              <DataGrid
                rows={regexRows}
                columns={regexColumns}
                pageSize={5}
                rowsPerPageOptions={[5]}
                disableSelectionOnClick
                components={{ Toolbar: GridToolbar }}
              />
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default HomePage;
