/* eslint-disable react/no-array-index-key */
/* eslint-disable react/jsx-props-no-spreading */
import React from 'react';
import PropTypes from 'prop-types';

import {
  useFlexLayout,
  useResizeColumns,
  useTable,
} from 'react-table';
import {
  Box,
  Flex,
  PseudoBox,
  Text,
  useColorMode,
} from '@chakra-ui/core';

const getStyles = (props, align = 'left') => [
  props,
  {
    style: {
      justifyContent: align === 'right' ? 'flex-end' : 'flex-start',
      alignItems: 'flex-start',
      display: 'flex',
      margin: '6px auto',
      paddingLeft: '3px',
    },
  },
];

const headerProps = (props, { column }) => getStyles(props, column.align);
const cellProps = (props, { cell }) => getStyles(props, cell.column.align);

const resizerProps = {
  position: 'absolute',
  top: 0,
  right: 0,
  width: '10px',
  height: '100%',
  zIndex: 1,
  style: { touchAction: 'none' },
};

const Table = ({
  columns,
  data,
  emptyMessage,
  onRowClick,
  ...rest
}) => {
  const { colorMode } = useColorMode();
  const defaultColumn = React.useMemo(
    () => ({
      // When using the useFlexLayout:
      minWidth: 30, // minWidth is only used as a limit for resizing
      width: 150, // width is used for both the flex-basis and flex-grow
      maxWidth: 200, // maxWidth is only used as a limit for resizing
    }),
    [],
  );

  const {
    getTableProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable(
    {
      columns,
      data,
      defaultColumn,
    },
    useResizeColumns,
    useFlexLayout,
    (hooks) => hooks.allColumns.push((elem) => elem),
  );

  return (
    <Box
      {...getTableProps()}
      flex={1}
      fontSize="sm"
      mt={1}
      border="1px solid #E2E8F0"
      borderRadius="4px"
      margin="auto 0"
      {...rest}
    >
      <Box overflowY="auto" overflowX="hidden">
        {headerGroups.map((headerGroup, i) => (
          <Flex
            flex={1}
            key={i}
            {...headerGroup.getHeaderGroupProps({})}
            backgroundColor="teal.500"
            color="white"
            fontWeight="bold"
          >
            {headerGroup.headers.map((column, i, cols) => (
              <Text
                as="div"
                key={i}
                {...column.getHeaderProps(headerProps)}
                textAlign="left"
                minHeight="24px"
              >
                {column.render('Header')}
                {column.canResize && i < cols.length - 1 && (
                  <Box {...resizerProps} {...column.getResizerProps()} />
                )}
              </Text>
            ))}
          </Flex>
        ))}
      </Box>
      <Box overflowY="scroll" overflowX="hidden">
        {rows.map((row) => {
          prepareRow(row);
          return (
            <PseudoBox
              display="flex"
              flex={1}
              key={row.id}
              data-rowindex={row.index}
              {...row.getRowProps()}
              onClick={onRowClick}
              cursor={onRowClick ? 'pointer' : undefined}
              _hover={{ bg: colorMode === 'dark' ? 'gray.700' : 'gray.100' }}
              minHeight="30px"
              lineHeight="30px"
              borderBottom="1px solid #E2E8F0"
            >
              {row.cells.map((cell) => (
                <Text
                  as="div"
                  key={`${row.id}_${cell.index}`}
                  wordBreak="break-all"
                  {...cell.getCellProps(cellProps)}
                >
                  {cell.render('Cell')}
                </Text>
              ))}
            </PseudoBox>
          );
        })}
      </Box>
      {rows.length === 0 && (<Text marginTop="6" textAlign="center">{emptyMessage}</Text>)}
    </Box>
  );
};

Table.propTypes = {
  columns: PropTypes.arrayOf(PropTypes.any).isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  data: PropTypes.object.isRequired,
  emptyMessage: PropTypes.string,
  onRowClick: PropTypes.func.isRequired,
};

Table.defaultProps = {
  emptyMessage: 'No se han encontrado resultados',
};

export default Table;
